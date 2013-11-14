#!/usr/bin/sh

DATASET=$HOME/hackaton/dataset/telegramas/www.resultados.gob.ar/telegramas
RESULTS=$DATASET-recon

NFIRST=10

find $DATASET -name *.pdf | head -$NFIRST > /tmp/pdf_telegramas.txt
for file in $(cat /tmp/pdf_telegramas.txt)
do
    BASENAME=$(basename ${file} .pdf)
    PDF_PATH=$(dirname ${file})
    OUT_PATH=$(echo $PDF_PATH | sed "s@$DATASET@$RESULTS@")

    echo "Processing ${file} ... "

# convierte pdf a pbm
    pdfimages ${file} /tmp/$BASENAME

# procesa telegrama
    mv /tmp/$BASENAME-000.pbm /tmp/$BASENAME.pbm
    python telegrama.py /tmp/$BASENAME.pbm

# guarda con la misma estructura de directorio que los pdf
    mkdir -p $OUT_PATH
    mv /tmp/$BASENAME-*.jpg $OUT_PATH/
done
