# Manual de zUtilidades

zUtilidades pretende ser un conjunto de pequeñas aplicaciones para NVDA.

Se intentara agregar aplicaciones que puedan ser de interés para que podamos consultarlas rápidamente y que a su vez sean de fácil manejo y claras en su interface.

zUtilidades tendrá un menú en Herramientas de NVDA, en ese menú se irán agregando los distintos módulos.

Cada modulo viene para poder agregarle una tecla rápida desde Gestos de entrada y una vez dentro buscar la categoría zUtilidades.

Por defecto los módulos vendrán sin ninguna tecla asignada.

Por lo tanto podremos lanzar los módulos o bien hiendo al menú de Herramientas / zUtilidades o asignando una combinación de teclas para cada módulo.

Actualmente esta formado por los siguientes módulos:

* Lanzador de aplicaciones.

# Modulo Lanzador de aplicaciones

Este módulo nos permitirá de manera rápida y desde cualquier parte de nuestro ordenador lanzar una aplicación ya sea portable o bien que se encuentre instalada.

## Pantalla principal

La pantalla principal consta de una lista de Categorías, una lista de Aplicaciones y un botón Menú.

Si tabulamos iremos recorriendo las distintas áreas.

### Lista de Categorías

En este área podremos añadir, editar o borrar una categoría pudiendo ordenar a nuestro gusto y en categorías nuestras aplicaciones.

Podemos acceder a las opciones añadir, editar o borrar de dos maneras.

Estando en el área categorías pulsando la tecla aplicaciones o en su defecto si no tuviésemos dicha tecla Shift+F10, se nos desplegara un menú donde podremos elegir una de las 3 opciones.

Los diálogos tanto de añadir como de editar son muy sencillos teniendo un único campo de texto donde poner el nombre de la nueva categoría o editar la categoría que elijamos, dos botones aceptar y Cancelar.

Si elegimos borrar tenemos que tener en cuenta que lo que contenga esa categoría se borrara por completo sin poder rehacer la acción, por lo tanto cuidado que podremos perder las aplicaciones que tengamos metidas en la base de datos y tendremos que volver hacerles la ficha.

Podemos también acceder a dichas opciones o bien tabulando hasta el botón Menú o con la combinación de tecla Alt+M. Si lo hacemos se nos desplegara un menú con un submenú llamado categorías donde podremos elegir una de las 3 opciones anteriores.

Comentar que editar y borrar siempre será sobre la categoría que tenga el foco, dando los correspondientes mensajes en caso de que no tengamos categorías.

También podremos con las combinaciones de teclas Alt + Flecha arriba y Flecha abajo mover la categoría para poder ordenarlas.

### Lista de Aplicaciones

En este área es donde se pondrán las aplicaciones correspondientes a la categoría que tengamos elegida.

Tenemos 3 opciones que es agregar, editar o borrar aplicaciones.

Podemos obtener estas opciones como en la lista de categorías ya sea con la tecla aplicaciones o en su caso Shift+F10 o dirigirse al botón Menú (Alt+M) y buscar el submenú Aplicaciones.

Si añadimos una aplicación hay dos campos que son obligatorios y es el nombre de la aplicación y el directorio donde se encuentre nuestra aplicación.

Actualmente soporta aplicaciones exe, bat y com.

Una vez rellenados los campos obligatorios podremos elegir si la aplicación requiere de parámetros adicionales o si la aplicación deseamos ejecutarla en modo administrador.

Si deseamos ejecutar una aplicación en modo administrador se nos pedirá el permiso correspondiente cuando lancemos la aplicación.

El dialogo de editar es exactamente el mismo que añadir pero nos permitirá modificar la entrada que elijamos.

Si borramos una entrada tenemos que tener en cuenta que la acción no será reversible.

En esta lista de aplicaciones podremos lanzar la aplicación que tenga el foco pulsando la tecla espaciadora.

También podremos con las combinaciones de teclas Alt + Flecha arriba y Flecha abajo mover la entrada para poder ordenarlas.

En este área podremos rápidamente navegar por las distintas entradas pulsando la primera letra de esa manera podremos encontrar rápidamente la aplicación que deseamos ejecutar si tenemos muchas en la base de datos.


### Botón Menú

Este botón será accesible desde cualquier parte de la interface pulsando la combinación Alt+M.

En este menú encontraremos 3 submenús que son Categoría, Aplicaciones y Hacer o restaurar copias de seguridad y una opción para salir.

Bien Categorías y aplicaciones ya lo explique por lo que explicare el submenú Hacer y restaurar copias de seguridad.

Bien si elegimos hacer una copia de seguridad se abrirá una ventana de guardar de Windows donde tendremos que elegir donde guardar nuestra copia de seguridad de la base de datos.

Bien el nombre del archivo es algo así por defecto:

Backup-03052021230645.zut-zl

Bien la extensión se pone por defecto y el nombre corresponde al modulo y contiene la fecha en que fue creado, decir que podemos poner el nombre que deseemos.

Una vez guardado podemos restaurarlo en caso que nuestra base de datos se corrompa o simplemente que la borremos por error o queramos volver a una versión que tengamos guardada.

Pues elegimos restaurar copias de seguridad y se nos abrirá una ventana clásica de Windows para abrir archivos.

Tenemos que elegir la copia que guardamos que tendrá la extensión *.zut-zl ojo no cambiar la extensión porque si no encontrara el archivo.
Una vez elegido se restaurara la copia de seguridad y cuando aceptemos se cerrara el complemento y la próxima vez que lo abramos ya tendrá nuestra copia restaurada.

Comentar que los archivos *.zut-zl son realmente archivos comprimidos pero cuidado con modificarlos por que si son modificados no coincidirá la firma y no dejara restaurarlos.

Con esto quiero decir que dichos archivos traen una firma que si no coincide a la hora de restaurar dará fallo y cada firma es diferente para cada archivo.

## Teclas rápidas

En las dos áreas tanto en la de categorías como en la de aplicaciones, podremos ordenar las entradas con:

* Alt + Flecha arriba o Flecha abajo

Cuando una categoría o aplicación llegue al principio o final se nos anunciara con un sonido distintivo para saber que no podemos ni subir ni bajar más.

* Alt + C: Nos llevara rápidamente al área de categorías.

* Alt + L: Nos llevara rápidamente a la lista de aplicaciones.

* Alt + M: Nos abrirá el menú.

* Tecla aplicaciones o Shift + F10: En las áreas de categoría y aplicaciones nos desplegara el menú con opciones.

* Espacio: En el área de lista de aplicaciones ejecutara la aplicación que tenga el foco.

* Escape: Cierra todos los diálogos que la aplicación puede abrir incluso la pantalla principal del Lanzador de aplicaciones, dejándonos el foco desde donde fue llamado.

## Observaciones del autor

Comentar varias cosas, la primera que el Lanzador de aplicaciones se cerrara cuando ejecutemos una aplicación, teniendo que llamarlo de nuevo cuando deseemos ejecutar otra.

E implementado también una función que guardara la posición de la categoría y de la aplicación ultima visitada por lo tanto cuando abramos el Lanzador de aplicaciones siempre quedarán elegidas tanto la ultima categoría como la ultima aplicación de dicha categoría.

También se implemento el guardado de foco, por lo que cuando llamemos el Lanzador de aplicaciones siempre nos dejara en la ultima posición donde estuvo el foco antes de cerrar.

Por poner un ejemplo si el foco esta en el botón menú y cerramos el Lanzador de aplicaciones, la próxima vez que lo abramos el foco se encontrara en el botón menú.

Estas características solo son validas durante la sesión de NVDA, esto quiere decir que si reiniciamos NVDA empezaremos con el foco en el área de categorías.

#Registro de cambios.
##Versión 0.1.

* Agregado modulo Lanzador de aplicaciones

* Versión inicial

