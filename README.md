#Extractor de Datos con IA, de manera en Red
## Este proyecto puede funcionar en la red, para que puedan acceder varios usuarios a traves de la red
## Funciona con una IA Local de Ollama, la cual se puede modificar en el archivo de "prompt_ia.py"
## Para que funcione bien, tiene que estar encendido como un servidor
## Por cada PDF es una factura, NO SE PUEDEN SUBIR VARIAS FACTURAS EN EL MISMO PDF, YA QUE CADA PDF ES UN REGISTRO EN EL EXCEL
## ESTE PROYECTO SOLO PUEDE EJECUTAR EL EXTRACTOR DE UNO A UNO,SI UN USUARIO LO EJECUTA Y ANTES QUE TERMINE, LO EJECUTA OTRO, SE ELIMINA EL EXCEL Y TODO DEL PRIMERO
## El funcionamiento paso a paso es el siguiente
### Se le cargan los PDFs en el index.html
### Cuando esta todo cargado, se le puede dar al boton de "Procesar" y comienza el proceso, a partir de aqui, el usuario solo podra ver un proceso para saber como va avanzando
### El servidor recoge los PDFs y se los pone en una carpeta
### El servidor va cogiendo un PDF, lo pasa a imagen, esto para que el OCR saque el texto del PDF
### Con el texto extraido, se le manda al "prompt_ia.py", que aparte de gestionar la IA, le crea un prompt con los datos que queremos extraer
### Cuando la IA nos devuelva los datos con un estilo de JSON, se van almacenando en una variable, la cual, al terminar, se convierte a un EXCEL y se guarda en la carpeta de salida
### Al usuario le tendria que salta automaticamente la descarga, pero igualmente tiene un boton para descargarlo manualmente en caso de fallo
### Con todo terminado, el servidor borra los pdfs que ha cogido, esto para no almacenar basura
