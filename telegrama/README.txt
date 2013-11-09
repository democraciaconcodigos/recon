Procesamiento de telegramas + OCR
=================================

1) Procesamiento de imágenes para facilitarle la vida al OCR
   -- Preprocesamiento de las imágenes (pdf)
   -- Correción de la orientación (enderezar los telegramas)
   -- identificar los campos manuscritos en el formulario para recortar el patch y mandarlo al OCR. 
	++ Nos vamos a centrar en los formularios de Córdoba, pero habría que pensar en algo más escalable
	++ Usar SVGs para definir los campos a mano sobre un telegrama de referencia. Ver que esquema conviene más.
	++ Ajustar el layout de referencia al detectado en cada imagen en particular para poder hacer un crop ajustado de los campos
   -- threads para procesar varios telegramas en paralelo

   (esto está casi todo mas o menos hecho, hay que pulirlo y probarlo en forma masiva)

2) OCR / machine learning
   -- Normalizar los patches / computar features (raw pixels, HOG, LBP)
   -- Probar tesseract sobre las imágenes de los patches directamente
   -- Separar dígitos y usar un esquema de reconocimiento propio (SVMs, kNN, etc) entrenado en MNIST
   -- Probar aumentar los conjuntos de entrenamiento para mejorar performance
   -- Detección de campos vacíos, guiones y/o demás no-dígitos

3) Consistencia, presentación y feedback
   -- Chequeo de consistencia (p.ej. la suma de de los votos = al total reportado)
   -- Se puede usar este tipo de chequeos de consistencia para mejorar el OCR?
   -- Como se pueden presentar los datos para que un usuario pueda validar o no el resultado. Grado de certidumbre en la detección? en el OCR?

