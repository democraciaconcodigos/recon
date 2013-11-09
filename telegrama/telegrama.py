#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from skimage import data, filter, transform, morphology, feature
from xml.dom import minidom

def sqdist(p0, p1):
    dx = p0[0] - p1[0]
    dy = p0[1] - p1[1]
    return dx*dx + dy*dy

## Lee una imagen para procesar por OCR
#
# @param file           path a la imagen
def load_image(file):

    # lee la imagen
    img = data.load(file)

    # la binariza en caso de que sea escala de grises
    if not img.dtype == 'bool':
        thr = filter.threshold_otsu(img)
        img = img > thr

    #si la proporcion de pixels en blanco es mayor a la mitad, la invierte
    if img.sum() > 0.5 * img.size:
        img = np.bitwise_not(img);

    return img

## Estimación del angulo de rotacion del formulario
#
# @param img                imagen binaria
# @param processing_scale   factor de escala que aplico a la imagen antes del procesamiento
def estimate_rotation(img):
    assert(img.dtype == 'bool')

    # elimina bloques rellenos para acelerar la deteccion de lineas
    elem = morphology.square(2)
    aux = morphology.binary_dilation(img, elem) - morphology.binary_erosion(img, elem)

    # Detección de lineas usando transformada de Hough probabilística
    maxgap = 2
    thres = 50
    rel_minlen = 0.1
    minlen = rel_minlen * min(aux.shape)
    lines = transform.probabilistic_hough(aux, threshold=thres, line_length=minlen, line_gap=maxgap)

    # me aseguro que el primer punto de cada línea sea el más próximo al origen
    for lin in lines:
        (x0,y0), (x1,y1) = lin
        if x1*x1+y1*y1 < x0*x0+y0*y0:
            (x0, x1) = (x1, x0)
            (y0, y1) = (y1, y0)

    # orientación dominante
    angle_half_range = np.math.pi / 4
    nbins = int(2 * angle_half_range * (180./np.math.pi) / 0.33)

    orient = []
    for lin in lines:
        (x0,y0), (x1,y1) = lin
        orient.append(np.math.atan2(y1-y0, x1-x0))

    (h, binval) = np.histogram(orient, range=(-angle_half_range, angle_half_range), bins=nbins)
    alpha = binval[h.argmax()] * (180./ np.math.pi)
    return alpha + 0.5 * (binval[1] - binval[0]) * (180./ np.math.pi)

## Rectifica imagen a la dirección dominante
#
# @param img            imagen
def rectify(img):
    # el rescalado la puede sacar de binaria
    if not img.dtype == 'bool':
        img = img > (img.max() - img.min()) / 2.0

    #estimacion de orientación
    alpha = estimate_rotation(img)

    # puede suceder de que tenga que rotar alpha+90
    return transform.rotate(img, angle=alpha, resize=True)

## Detección de lineas horizontales y verticales
#
# @param img            imagen
def detect_lines(img):
    minsize = min(img.shape)
    maxsize = max(img.shape)

    # Detección de lineas usando transformada de Hough probabilística
    minlen = 0.1 * minsize
    maxgap = 0.1 * minlen
    angles = np.array([0, np.math.pi/2]) # asume imagen rectificada
    lines = transform.probabilistic_hough(img, theta=angles, threshold=10, line_length=minlen, line_gap=maxgap)

    # separa líneas verticales y horizontales
    vlines = []
    hlines = []
    for lin in lines:
        p0, p1 = lin
        (x0, y0) = p0
        (x1, y1) = p1
        linlen = np.math.sqrt(sqdist(p0, p1))
        if linlen > minsize:
            continue
        xc, yc = 0.5*(x0+x1), 0.5*(y0+y1)
        lin_info = [x0, y0, x1, y1, xc, yc, linlen]
        if x0 == x1:
            if y1 > y0:
                lin_info[1], lin_info[3] = lin_info[3], lin_info[1]
            vlines.append(lin_info)
        else:
            if x1 > x0:
                lin_info[0], lin_info[2] = lin_info[2], lin_info[0]
            hlines.append(lin_info)

    # filtrado de líneas duplicadas
    dthr = 0.01 * minsize
    dthr = dthr * dthr

    for lines in (vlines, hlines):
       i = 0
       while i < len(lines):
           l1 = lines[i]

           acc = np.array(l1)
           nacc = 1.0

           j = i+1
           while j < len(lines):
               l2 = lines[j]
               d1 = sqdist(l1[0:2], l2[0:2])
               d2 = sqdist(l1[2:4], l2[2:4])
               # ambos extremos están muy próximos entre si
               if d1 < dthr and d2 < dthr:
                   acc = acc + np.array(l2)
                   nacc = nacc + 1.0
                   lines.pop(j)
               else:
                   j = j+1

           lines[i] = (acc/nacc).tolist()
           lines[i][4] = 0.5 * (lines[i][0]+lines[i][2])
           lines[i][5] = 0.5 * (lines[i][1]+lines[i][3])
           lines[i][6] =  np.math.sqrt(sqdist((lines[i][0],lines[i][1]), (lines[i][2],lines[i][3])))
           i = i+1

    # # ordena por longitud decreciente
    # vlines = sorted(vlines, key=lambda a_entry: a_entry[6])
    # vlines = vlines[::-1]
    # hlines = sorted(hlines, key=lambda a_entry: a_entry[6])
    # hlines = hlines[::-1]

    return hlines, vlines

## Detección de palabra clave
#
# @param img            imagen
# @param template       patch de referencia
def detect_keypatch(img, template):
    simg = feature.match_template(img, template, pad_input=True)
    simg = simg.clip(0, simg.max())
    rel_thr = 0.75
    peaks = feature.peak_local_max(simg, min_distance=5, threshold_abs=rel_thr*(simg.max()-simg.min()), exclude_border=False)
    ht, wt = template.shape
    for i in range(len(peaks)):
        peaks[i] = [peaks[i][1]-wt/2, peaks[i][0]-ht/2]

    return peaks

## Extracción de "quads" a partir de líneas horizontales y verticales
#
# @param svg_file        modelo
'''
     (A)     HL0        (B)
      +------------------+
      |
      |
      |
      | VL0
      |
      |
      |      HL1
      +------------------+
     (C)                (D)
'''
def detect_quads(hlines, vlines):

    dthr = 10 #0.1 * np.min(vlines[:][6])
    dthr = dthr*dthr

    quads = []

    for vl0 in vlines:
        vl0_p0 = vl0[0:2]

        hl0_hyp = []
        for hl0 in hlines:
            hl0_p0 = hl0[0:2]
            if sqdist(vl0_p0, hl0_p0) < dthr:
                hl0_hyp.append(hl0)

        if len(hl0_hyp)==0:
            continue

        vl0_p1 = vl0[2:4]

        hl1_hyp = []
        for hl1 in hlines:
            hl1_p0 = hl1[0:2]
            if sqdist(vl0_p1, hl1_p0) < dthr:
                hl1_hyp.append(hl1)

        if len(hl1_hyp)==0:
            continue

        for vl1 in vlines:
            vl1_p0 = vl1[0:2]
            vl1_p1 = vl1[2:4]
            for hl0 in hl0_hyp:
                hl0_p1 = hl0[2:4]
                if sqdist(vl1_p0, hl0_p1) < dthr:
                    for hl1 in hl1_hyp:
                        hl1_p1 = hl1[2:4]
                        if sqdist(vl1_p1, hl1_p1) < dthr:
                            quads.append(vl0_p0 + vl1_p1)
                            break

    for q in quads:
        if q[0] > q[2]:
            q[0], q[2] = q[2], q[0]
        if q[1] > q[3]:
            q[1], q[3] = q[3], q[1]

    return quads

## Lectura de modelo a partir de archivo .svg
#
# @param svg_file        modelo
def parse_model(svg_file):
    doc = minidom.parse(svg_file)
    model = []
    x0, y0 = 0., 0.
    for rect in doc.getElementsByTagName('rect'):
        x = float(rect.getAttribute('x'))
        y = float(rect.getAttribute('y'))
        width = float(rect.getAttribute('width'))
        height = float(rect.getAttribute('height'))
        id = rect.getAttribute('id').lstrip()
        if id.find("ID_") == 0:
            id = id[3:]
            #model.append({'x':x, 'y':y, 'width':width, 'height':height, 'id':str(id)})
            model.append([x, y, width, height, id])
            if id=="TELEGRAMA":
                x0, y0 = x, y

    svg = doc.getElementsByTagName('svg')
    svg_height = float(svg[0].getAttribute('height'))

    # refiere todo al patch de referencia
    for i in range(len(model)):
        model[i][0] = model[i][0] - x0
        model[i][1] = model[i][1] - y0

    return model

# ----------------------------------------------------------------------

import os, sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm

PATH = os.path.dirname(os.path.abspath(__file__))

#image_file = path+'/040240351_7634.pbm'
#image_file = PATH+'/040010002_0052.pbm'
#image_file = path+'/030010001_0001.pbm'
keyword_file = PATH+'/model/keyword.pbm'
model_file = PATH+'/model/cordoba.svg'


def main():
    try:
        image_file = os.path.join(PATH, sys.argv[1])
        process_telegram(image_file)
    except Exception:
        print >>sys.stderr, "Falta el nombre del telegrama.\n"
        return 0

def process_telegram(image_file):
    # levanta imagen
    img1 = load_image(image_file)

    # achico la imagen para acelerar el procesamiento
    processing_scale = 0.5
    img2 = transform.rescale(img1, processing_scale)
    img2 = img2 > 0

    # operaciones morfológicas (preproc.)
    elem = morphology.square(2)
    #img2 = morphology.binary_dilation(img2, elem)
    img2 = morphology.remove_small_objects(img2, min_size=64, connectivity=8)

    # rectificación
    img3 = rectify(img2)

    # detección de lineas horiz y vert
    hlines, vlines = detect_lines(img3)

    # detección de la palabra TELEGRAMA
    keypatch = load_image(keyword_file)
    keypatch = transform.rescale(keypatch, processing_scale)
    peaks = detect_keypatch(img3, keypatch)
    hk, wk = keypatch.shape

    # cuadriláteros
    quads = detect_quads(hlines, vlines)

    # modelo de formulario
    x0, y0 = peaks[0]
    model = parse_model(model_file)
    for i in range(len(model)):
        model[i][0] = model[i][0] * processing_scale + x0
        model[i][1] = model[i][1] * processing_scale + y0
        model[i][2] = model[i][2] * processing_scale
        model[i][3] = model[i][3] * processing_scale

    # Overlap de cuadrilateros y modelo
    overlap = []
    for i in range(len(quads)):
        overlap.append([0] * len(model))

    for i in range(len(quads)):
        x1q, y1q, x2q, y2q = quads[i][0:4]
        area_q = (y2q - y1q) * (x2q - x1q)
        for j in range(len(model)):
            x1m, y1m, x2m, y2m = model[j][0], model[j][1], model[j][0]+model[j][2]-1.0, model[j][1]+model[j][3]-1.0
            area_m = (y2m - y1m) * (x2m - x1m)

            x1_inter = max(x1q, x1m)
            x2_inter = min(x2q, x2m)
            y1_inter = max(y1q, y1m)
            y2_inter = min(y2q, y2m)

            if y2_inter > y1_inter and x2_inter > x1_inter:
                area_inter = (y2_inter - y1_inter) * (x2_inter - x1_inter)
                area_union = area_q + area_m - area_inter
                overlap[i][j] = np.math.sqrt(area_inter / area_union)

    # probar con el de máximo overlap en el caso de que haya muchas detección
    min_match_overlap = 0.75
    src, dst = [], []
    for i in range(len(quads)):
        x1q, y1q, x2q, y2q = quads[i][0:4]
        for j in range(len(model)):
            x1m, y1m, x2m, y2m = model[j][0], model[j][1], model[j][0]+model[j][2]-1.0, model[j][1]+model[j][3]-1.0
            if overlap[i][j] < min_match_overlap:
                src.append([x1q, y1q])
                src.append([x2q, y2q])
                dst.append([x1m, y1m])
                dst.append([x2m, y2m])

    tform = transform.estimate_transform('similarity', np.array(src), np.array(dst))
    img4 = transform.warp(img3, inverse_map=tform.inverse)

    # visualizacion
    plt.close('all')
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)

    #imagen original
    ax1.imshow(img1, cmap=cm.Greys_r)
    ax1.set_axis_off()

    #imagen rectificada
    ax2.imshow(img3, cmap=cm.Greys_r)
    ax2.set_axis_off()

    ax3.imshow(img3, cmap=cm.Greys_r)
    ax3.set_axis_off()

    # lineas verticales
    for lin in vlines:
        x0, y0, x1, y1 = lin[0:4]
        feat = plt.Line2D((x0, x1), (y0, y1), color='g', linewidth=2)
        ax2.add_line(feat)

    # lineas horizontales
    for lin in hlines:
        x0, y0, x1, y1 = lin[0:4]
        feat = plt.Line2D([x0, x1], [y0, y1], color='b', linewidth=1)
        ax2.add_line(feat)

    #palabra clave
    for pk in peaks:
        x, y = pk[0], pk[1]
        feat = plt.Rectangle((x, y), wk, hk, edgecolor='r', facecolor='none', linewidth=2)
        ax2.add_patch(feat)

    #quads
    for q in quads:
        rect = plt.Rectangle((q[0], q[1]), q[2]-q[0], q[3]-q[1], edgecolor='yellow', facecolor='none', linewidth=2)
        ax3.add_patch(rect)

    #fields
    x0, y0 = peaks[0]
    for field in model:
        x, y = field[0], field[1]
        w, h = field[2], field[3]
        feat = plt.Rectangle((x, y), w, h, edgecolor='r', facecolor='none', linewidth=1)
        ax3.add_patch(feat)

    plt.show()


if __name__ == "__main__":
    sys.exit(main())
