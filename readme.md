# Manual de zUtilidades

zUtilidades pretende ser un conjunto de pequeñas aplicaciones para NVDA.

Se intentara agregar aplicaciones que puedan ser de interés para que podamos consultarlas rápidamente y que a su vez sean de fácil manejo y claras en su interface.

zUtilidades tendrá un menú en Herramientas de NVDA, en ese menú se irán agregando los distintos módulos.

Cada modulo viene para poder agregarle una tecla rápida yendo al menú de NVDA / Preferencias / Gestos de entrada y una vez dentro buscar la categoría zUtilidades.

Por defecto los módulos vendrán sin ninguna tecla asignada.

Por lo tanto podremos lanzar los módulos o bien hiendo al menú de Herramientas / zUtilidades o asignando una combinación de teclas para cada módulo.

Actualmente esta formado por los siguientes módulos:

* Lanzador de aplicaciones.
* Notas rápidas.

# Modulo Lanzador de aplicaciones

Este módulo nos permitirá de manera rápida y desde cualquier parte de nuestro ordenador lanzar una aplicación ya sea portable o bien que se encuentre instalada.

## Pantalla principal

La pantalla principal consta de una lista de categorías, una lista de aplicaciones y un botón Menú.

Si tabulamos iremos recorriendo las distintas áreas.

### Lista de categorías

En este área podremos añadir, editar o borrar una categoría pudiendo ordenar a nuestro gusto y en categorías nuestras aplicaciones.

Podemos acceder a las opciones Añadir, Editar o Borrar de dos maneras.

Estando en el área Categorías pulsando la tecla Aplicaciones o en su defecto si no tuviésemos dicha tecla Shift+F10, se nos desplegara un menú donde podremos elegir una de las 3 opciones.

Los diálogos tanto de añadir como de editar son muy sencillos teniendo un único campo de texto donde poner el nombre de la nueva categoría o editar la categoría que elijamos, dos botones Aceptar y Cancelar.

Si elegimos borrar tenemos que tener en cuenta que lo que contenga esa categoría se borrara por completo sin poder rehacer la acción, por lo tanto cuidado que podremos perder las aplicaciones que tengamos metidas en la base de datos y tendremos que volver a introducir todas las aplicaciones o comandos o accesos que tuviese esa categoría.

Podemos también acceder a dichas opciones o bien tabulando hasta el botón Menú o con la combinación de tecla Alt+M. Si lo hacemos se nos desplegara un menú con un submenú llamado Categorías donde podremos elegir una de las 3 opciones anteriores.

Comentar que Editar y Borrar siempre será sobre la categoría que tenga el foco, dando los correspondientes mensajes en caso de que no tengamos categorías.

También podremos con las combinaciones de teclas Alt + Flecha arriba y Flecha abajo mover la categoría para poder ordenarlas.

### Lista de aplicaciones

En este área es donde se pondrán las aplicaciones correspondientes a la categoría que tengamos elegida.

Tenemos 3 opciones que son Añadir acción, Editar acción o Borrar acción.

Podemos obtener estas opciones como en la lista de categorías ya sea con la tecla Aplicaciones o en su caso Shift+F10 o dirigirse al botón Menú (Alt+M) y buscar el submenú Aplicaciones.

En esta lista de aplicaciones podremos lanzar la aplicación que tenga el foco pulsando la tecla espaciadora.

También podremos con las combinaciones de teclas Alt + Flecha arriba y Flecha abajo mover la entrada para poder ordenarlas.

En este área podremos rápidamente navegar por las distintas entradas pulsando la primera letra de esa manera podremos encontrar rápidamente la aplicación que deseamos ejecutar si tenemos muchas en la base de datos.

#### Menú Añadir acción

En este menú podremos elegir entre las siguientes opciones:

* Añadir aplicación:

Si añadimos una aplicación hay dos campos que son obligatorios y es el nombre de la aplicación y el directorio donde se encuentre nuestra aplicación.

Actualmente el complemento soporta aplicaciones con las extensiones exe, bat y com.

Una vez rellenados los campos obligatorios podremos elegir si la aplicación requiere de parámetros adicionales o si la aplicación la deseamos ejecutar en modo administrador.

Si deseamos ejecutar una aplicación en modo administrador se nos pedirá el permiso correspondiente cuando lancemos la aplicación. 

* Añadir comando CMD

En este dialogo podremos agregar comandos de consola.

	Los campos nombre para identificar el comando y el campo comandos son obligatorios.

Bien varias apreciaciones, aparte de lanzar comandos cmd si dominamos Windows PowerShell si ponemos en la línea de comandos PowerShell y seguido de lo que queremos ejecutaremos también comandos PowerShell.

Igualmente si son comandos CMD añado que podemos ejecutar varias líneas las cuales tienen que ir separadas por el símbolo (et) que se consigue haciéndolo con Shift+6, esto con un teclado QWERTY español. Si se usa un teclado QWERTY inglés, esto se hará con Shift+7.

Pongo un ejemplo de la línea de comandos para reiniciar el explorador de Windows, comprobareis que uso el símbolo (et) para separar una línea de comandos por otra.

`taskkill /f /im explorer.exe & start explorer`

También en este dialogo podemos poner una pausa para que no se cierre la consola y a si poder ver los resultados.

También podemos ejecutar como administrador.

* Añadir accesos a carpetas

En este dialogo tendremos que elegir un nombre para identificar el acceso a la carpeta y elegir una carpeta.

Esto nos permitirá abrir rápidamente carpetas de nuestro sistema desde cualquier parte.

* Añadir ejecutar accesos directos de Windows

En este dialogo podremos elegir un acceso directo para lanzarlo. También podremos elegir si lo queremos lanzar como administrador.

Los campos para identificar el nombre del acceso directo y la ruta son obligatorios.

* Añadir aplicación instalada

En este dialogo se obtendrán todas las aplicaciones instaladas en nuestro ordenador ya sea por el usuario o aplicaciones que ya vienen con Windows.

También en esta pantalla podremos elegir las aplicaciones instaladas desde la tienda de Windows.

Advertencia esto no es válido para Windows 7.

Bien una vez añadida una aplicación desde este dialogo comentar que no puede ser editado, teniendo que borrar la entrada si queremos añadirlo de nuevo.

La opción administrador en este dialogo no funcionara para todas las aplicaciones. Funcionando solo para aquellas que permita elevar privilegios de administrador.

Avisar también que en este dialogo en el cuadro combinado también saldrán aquellos accesos instalados por las aplicaciones, podremos elegirlos pero puede que alguno no permita abrirse dando error.

Comentar también que hay que tener cuidado por que en este listado saldrán aplicaciones que pueden ser para administrar o aplicaciones de gestión que si no sabemos para que son es mejor no tocarlas.

#### Editar acción

El dialogo de Editar es exactamente el mismo que Añadir acción pero nos permitirá modificar la entrada que elijamos.

Nos permitirá modificar todos los elementos menos los añadidos por la opción Añadir aplicación instalada, los diálogos serán los mismos que en las opciones para añadir.

#### Borrar acción

Si borramos una entrada tenemos que tener en cuenta que la acción no será reversible.

### Botón Menú

Este botón será accesible desde cualquier parte de la interface pulsando la combinación Alt+M.

En este menú encontraremos cuatro submenús que son Categorías, Acciones, Hacer o restaurar copias de seguridad y Opciones, en este menú también encontramos la opción Salir.

Bien Categorías y Acciones ya lo explique por lo que explicare el submenú Hacer y restaurar copias de seguridad y Opciones.

Bien si elegimos Hacer una copia de seguridad se abrirá una ventana de guardar de Windows donde tendremos que elegir donde guardar nuestra copia de seguridad de la base de datos.

Bien el nombre del archivo es algo así por defecto:

`Backup-03052021230645.zut-zl`

Bien la extensión se pone por defecto y el nombre corresponde al modulo y contiene la fecha en que fue creado, decir que podemos poner el nombre que deseemos.

Una vez guardado podemos restaurarlo en caso que nuestra base de datos se corrompa o simplemente que la borremos por error o queramos volver a una versión que tengamos guardada.

Pues elegimos Restaurar copias de seguridad y se nos abrirá una ventana clásica de Windows para abrir archivos.

Tenemos que elegir la copia que guardamos que tendrá la extensión *.zut-zl ojo no cambiar la extensión porque si no encontrara el archivo.
Una vez elegido se restaurara la copia de seguridad y cuando pulsamos en Aceptar  se cerrara el complemento y la próxima vez que lo abramos ya se tendrá nuestra copia restaurada.

Comentar que los archivos *.zut-zl son realmente archivos comprimidos pero cuidado con modificarlos por que si son modificados no coincidirá la firma y no dejara restaurarlos.

Con esto quiero decir que dichos archivos traen una firma que si no coincide a la hora de restaurar dará fallo y cada firma es diferente para cada archivo.

En el submenú de Opciones ahora solo está la opción Volver a valores por defecto el lanzador de aplicaciones.

Si elegimos esta opción se borrara toda la base de datos dejando el complemento como si fuese recién instalado.

## Teclas rápidas

En las dos áreas tanto en la de Categorías como en la de Aplicaciones, podremos ordenar las entradas con:

* Alt + Flecha arriba o Flecha abajo

Cuando una categoría o aplicación llegue al principio o final se nos anunciara con un sonido distintivo para saber que no podemos ni subir ni bajar más.

* Alt + C: Nos llevara rápidamente al área de categorías.

* Alt + L: Nos llevara rápidamente a la lista de aplicaciones.

* Alt + M: Nos abrirá el menú.

* Tecla aplicaciones o Shift + F10: En las áreas de categoría y aplicaciones nos desplegara el menú contextual con opciones.

* Espacio: En el área de lista de aplicaciones ejecutara la aplicación que tenga el foco.

* Escape: Cierra todos los diálogos que la aplicación puede abrir incluso la pantalla principal del Lanzador de aplicaciones, dejándonos el foco desde donde fue llamado.

## Observaciones del autor

Comentar varias cosas, la primera que el Lanzador de aplicaciones se cerrara cuando ejecutemos una aplicación, teniendo que llamarlo de nuevo cuando deseemos ejecutar otra.

E implementado también una función que guardara la posición de la categoría y de la aplicación ultima visitada por lo tanto cuando abramos el Lanzador de aplicaciones siempre quedarán elegidas tanto la ultima categoría como la ultima aplicación de dicha categoría.

También se implemento el guardado de foco, por lo que cuando llamemos el Lanzador de aplicaciones siempre nos dejara en la ultima posición donde estuvo el foco antes de cerrar.

Por poner un ejemplo si el foco esta en el botón Menú y cerramos el Lanzador de aplicaciones, la próxima vez que lo abramos el foco se encontrara en el botón Menú.

Estas características solo son validas durante la sesión de NVDA, esto quiere decir que si reiniciamos NVDA empezaremos con el foco en el área de categorías.

Este complemento esta echo para usarse con Windows 10, por lo que si está usando versiones anteriores y tiene algún problema coméntelo pero seguramente no podre hacer nada ya que algunas características solo se encuentran en Windows 10.

# Modulo Notas rápidas

Este módulo nos servirá para tener a mano pequeñas notas las cuales podremos consultar, editar, borrar.

Este modulo tiene el mismo manejo que el Lanzador de aplicaciones pero varia en algunas teclas explicadas a continuación.

No voy a volver a explicar el menú con el cual podremos hacer copias de seguridad, restaurarlas, volver a valores por defecto el complemento, manejar categorías y notas.

Tampoco voy a volver a explicar el recorrido de la interface principal ya que es exactamente lo mismo.

Podremos añadir una nota rápida y en el dialogo que se abre podremos poner el titulo de la nota y si tabulamos el contenido.

El dialogo de editar nota es exactamente lo mismo, poner un titulo o modificar el que ya esta y poder editar la nota.

Este modulo se diferencia con el de lanzador de aplicaciones en que usa algunas nuevas combinaciones de teclas.

* F1: Cuando estemos encima de una nota si presionamos F1 nos leerá el contenido de la nota.
* Shift+C: Nos copiara la nota enfocada al portapapeles para que podamos copiarla en cualquier sitio.
* Shift+V: Esta combinación nos cerrara la ventana de notas rápidas y pegara el contenido de la nota que tuviésemos enfocado en el foco.

Esto significa que si llamamos a notas rápidas desde el bloc de notas o un asunto de un email cuando presionemos esta combinación el texto se pegara donde teníamos el foco.

Cuidado si estamos en el escritorio o algún sitio donde no se pueda pegar directamente no hará nada.

También sigue funcionando tanto en el área de categorías como en el área de lista de notas el poder ordenar dichas áreas con Alt+Flechas arriba y abajo para mover lo que tengamos seleccionado.

Si pulsamos espacio se abrirá una ventana donde podremos solo visualizar nuestra nota.

Decir que este modulo viene sin tecla rápida definida, por lo que tendremos que agregársela en Gestos de entrada.

# Agregar una nota rápida desde cualquier lugar

También el modulo de Notas rápidas tiene una característica para agregar notas rápidas desde cualquier sitio sin necesidad de abrir el complemento para añadir.

En el gestor de gestos de entradas ahora podremos configurar una nueva combinación de teclas que encontrareis en:

NVDA / Preferencias / Gestos de entrada / zUtilidades / Agregar una nota rápida del texto seleccionado

Cuando tengamos ya una combinación asignada solo tendremos que seleccionar un texto en cualquier parte y pulsar la combinación de teclas.

Se abrirá una ventana en la cual lo primero que tendremos que elegir es en que categoría queremos guardar nuestra nota, solo nos aparecerán las categorías que tengamos añadidas.

Si tabulamos caeremos en el campo para poner el titulo de la nota y si volvemos a tabular tendremos el texto que habíamos seleccionado.

Si aceptamos se guardara y ya tendremos nuestra nota en nuestra categoría que hallamos elegido.

# Menús Virtuales para el Lanzador de aplicaciones y para Notas rápidas

Bien estos menús vienen a potenciar a zUtilidades haciendo que ahora sea mucho más productivo y más rápido.

Bien los gestos que tengamos asignados al lanzador de aplicaciones y a notas rápidas ahora tienen una doble pulsación.

Si pulsamos una sola vez dicha combinación nos saldrá la interface gráfica, si pulsamos dos veces nos saldrá el menú virtual.

Bien en dicho menú nos podremos mover con flechas izquierda y derecha entre categorías y con flechas arriba y abajo entre ítems de dicha categoría si los hay.

Bien existen algunas diferencias entre el menú del lanzador de aplicaciones y el de notas rápidas.

En el menú virtual de lanzador de aplicaciones con las flechas nos movemos y con intro ejecutamos el item que tengamos seleccionado haciendo la acción que corresponda.

Si es un comando cmd pues lo ejecutara, si es un acceso rápido lo mismo y así como si fuese la interface grafica.

Bien con Escape saldremos del menú si no queremos hacer nada.

También nos podemos mover por las categorías pulsando las teclas de inicio del nombre salvo la ñ que no la admite este menú todas las demás nos llevara rápidamente a la categoría.

Bien también si dicha letra no tiene una categoría nos dará el mensaje de ayuda al igual que si pulsamos cualquier otra tecla que sea diferente a las mencionadas.

Decir que mientras el menú este activo todas las demás combinaciones de teclas de NVDA no funcionarán hasta que no salgamos del menú.

En el menú de notas rápidas la tecla espaciadora no vale para nada y si tiene diferencias con el del lanzador de aplicaciones.

Cuando estemos encima de un item si pulsamos F1 nos hablara el contenido de la nota, con Shift+C nos pegara la nota al portapapeles y con Shift+V nos pegara el contenido de la nota donde tengamos el foco.

Igualmente lo dicho mientras el menú este activo tiene prioridad hasta que no salgamos en el teclado.

## Traductores y colaboradores:

* Francés: Rémy Ruiz
* Portugués: Ângelo Miguel Abrantes
* Javi Domínguez: Mil gracias por enseñarme a programar el menú. Mejor dicho por explicarlo para tontos como yo.
# Registro de cambios.
## Versión 0.2.

* Se corrigieron muchos errores internos.
* Se estabilizo el modulo Lanzador de aplicaciones.
* Se agrego un nuevo módulo de Notas rápidas.
* Se agregaron menús virtuales para los dos módulos.

## Versión 0.1.6.

* Agregado idioma Francés y  Portugués (Portugal / Brasil).

## Versión 0.1.5.

* Restructurados los menús.

Agregado la posibilidad de añadir:

* Añadir comando CMD

* Añadir accesos a carpetas

* Añadir ejecutar accesos directos de Windows

* Añadir aplicación instalada

* Se agrego en el botón Menú la posibilidad en Opciones Volver a valores por defecto el lanzador de aplicaciones

* Se corrigieron distintos errores con la base de datos.

* Se corrigieron errores internos.

* Se preparo el complemento para ser traducido.

## Versión 0.1.

* Agregado modulo Lanzador de aplicaciones

* Versión inicial.

