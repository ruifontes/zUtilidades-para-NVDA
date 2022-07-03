# Руководство по zUtility

* Автор: Гектор Дж.
* Поддержка NVDA: с 2019.3 по 2021.1
* [Загрузка плагина:] (https://nvda.es/files/get.php?file=zUtilidades)
* [Проект на GitHub:](https://github.com/hxebolax/zUtilidades-para-NVDA)

---

Индекс < а id= "индекс" > < / а>
-------------
- [Введение](#mark0)
- [Модуль запуска приложений](#mark1)
- [Главный экран] (#mark2)
- [Список категорий](#mark3)
- [Список приложений](#mark4)
- [Меню " Добавить действие](#mark5)

- [Редактировать действие] (#mark6)
- [Удалить действие] (#mark7)
- [Кнопка Меню] (#mark8)
- [Горячие клавиши] (#mark9)
- [Комментарии автора] (#mark10)
- [Модуль быстрые заметки] (#mark11)
- [Добавить быструю заметку из любого места] (#mark12)
- [Виртуальные меню для запуска приложений и для быстрых заметок] (#mark13)
- [Переводчики и сотрудники] (#mark14)
- [Журнал изменений](#mark15)
- [Версия 0.2.3] (#mark0.2. 3)
- [Версия 0.2.2] (#mark0. 2.2)
- [Версия 0.2.1] (#mark0.2. 1)
- [Версия 0.2](#mark0.2)

- [Версия 0.1.6] (#mark0.1. 6)
- [Версия 0.1.5] (#mark0.1. 5)
- [Версия 0.1](#mark0.1)

---

# Введение < а id= "mark0" >< / а>

zutibility предназначен для набора небольших приложений для NVDA.

Мы попытаемся добавить приложения, которые могут представлять интерес, чтобы мы могли быстро просматривать их и, в свою очередь, просты в управлении и понятны в их интерфейсе.

zutibility будет иметь меню в NVDA Tools, в это меню будут добавлены различные модули.

Каждый модуль приходит для того чтобы добавить к нему 
один Горячий Ключ, перейдя в меню NVDA / настройки / жесты ввода и один раз внутри искать категорию zutibility.

По умолчанию модули будут поставляться без каких-либо назначенных клавиш.

Таким образом, вы можете запустить модули либо перейдя в меню инструментов / zutibility или назначив комбинацию клавиш для каждого модуля.

В настоящее время он состоит из следующих модулей:

* Запуск приложений.
* Быстрые заметки.

# Модуль запуска приложений < а id= "mark1" > < / а>

Этот модуль 
это позволит нам быстро и из любого места на нашем компьютере запустить портативное или установленное приложение.

## Главный экран < а id= "mark2" > < / а>

Главный экран состоит из списка категорий, списка приложений и кнопки Меню.

Если мы будем табулировать, мы будем путешествовать по различным областям.

### Список категорий < А id= "mark3" > < / а>

В этой области вы можете добавлять, редактировать или удалять категорию, сортируя по своему вкусу и по нашим категориям 
применение.

Мы можем получить доступ к параметрам добавить, редактировать или удалять двумя способами.

Находясь в области категории, нажав клавишу Applications или в противном случае, если у нас не было этой клавиши Shift+F10, мы развернем меню, где мы можем выбрать один из 3 вариантов.

Диалоги как для добавления, так и для редактирования очень просты, имея одно текстовое поле, где можно указать имя новой категории или изменить выбранную нами категорию, две кнопки OK и cancel.

Если мы решим удалить 
мы должны иметь в виду, что то, что содержит эту категорию, будет полностью удалено без возможности повторить действие, поэтому будьте осторожны, что мы можем потерять приложения, которые у нас есть в базе данных, и нам придется повторно ввести все приложения или команды или доступы, которые имели эту категорию.

Мы также можем получить доступ к этим параметрам либо путем табуляции до кнопки меню, либо с помощью комбинации клавиш Alt+M. Если мы это сделаем, мы развернем меню с подменю с именем 
Категории, где вы можете выбрать один из 3 вариантов выше.

Комментарий, что редактирование и удаление всегда будет о категории, которая имеет фокус, давая соответствующие сообщения, если у нас нет категорий.

Вы также можете с помощью комбинаций клавиш Alt + стрелка вверх и Стрелка вниз переместить категорию, чтобы иметь возможность сортировать их.

### Список приложений < а id= "mark4" > < / а>

В этой области будут размещены приложения, соответствующие выбранной нами категории.


У нас есть 3 варианта, которые добавить действие, изменить действие или удалить действие.

Мы можем получить эти параметры, как в списке категорий либо с помощью клавиши Applications или в вашем случае Shift+F10 или перейти к кнопке меню (Alt+M) и найти подменю Applications.

В этом списке приложений вы можете запустить приложение с фокусом, нажав клавишу пробела.

Вы также можете с помощью комбинаций клавиш Alt + стрелка вверх и Стрелка вниз переместить вход, чтобы отсортировать их.

В этом 
область вы можете быстро просматривать различные записи, нажав на первую букву, так что вы можете быстро найти приложение, которое вы хотите запустить, если у нас есть много в базе данных.

#### Меню Добавить действие < к id= "mark5" >< / к>

В этом меню вы можете выбрать один из следующих вариантов:

* Добавить приложение:

Если мы добавляем приложение есть два поля, которые являются обязательными, и это имя приложения и каталог, где находится наше приложение.

В настоящее время плагин 
поддержка приложений с расширениями exe, bat и com.

После заполнения обязательных полей мы можем выбрать, требует ли приложение дополнительных параметров или мы хотим запустить приложение в режиме администратора.

Если мы хотим запустить приложение в режиме администратора, нам будет предложено соответствующее разрешение при запуске приложения. 

* Добавить команду CMD

В этом диалоге мы можем добавлять консольные команды.

	Поля имя для идентификации команды и поля команды 
они обязательны.

Ну несколько оценок, кроме запуска команд cmd, если мы освоим Windows PowerShell, если мы помещаем в командной строке PowerShell, а затем то, что мы хотим, мы также будем запускать команды PowerShell.

Точно так же, если это команды CMD, я добавляю, что мы можем выполнить несколько строк, которые должны быть разделены символом (et), который достигается с помощью Shift+6, это с испанской QWERTY-клавиатурой. Если используется английская QWERTY-клавиатура, это будет сделано с помощью Shift+7.

Я ставлю 
пример командной строки чтобы перезапустить Проводник Windows, вы убедитесь, что я использую символ (et), чтобы отделить одну командную строку от другой.

'taskkill / f / im explorer.exe & start explorer`

Также в этом диалоге мы можем поставить паузу, чтобы консоль не закрывалась и не могла видеть результаты.

Мы также можем работать от имени администратора.

* Добавить доступ к папкам

В этом диалоге нам нужно будет выбрать имя, чтобы определить доступ к папке и выбрать папку.


Это позволит нам быстро открывать папки в нашей системе из любого места.

* Добавить запуск ярлыков Windows

В этом диалоге вы можете выбрать ярлык для запуска. Мы также можем выбрать, хотим ли мы запустить его в качестве администратора.

Поля для идентификации имени ярлыка и пути являются обязательными.

* Добавить установленное приложение

В этом диалоге вы получите все приложения, установленные на нашем компьютере либо пользователем или приложениями 
они уже поставляются с Windows.

Также на этом экране вы можете выбрать приложения, установленные из магазина Windows.

Предупреждение это недопустимо для Windows 7.

Ну после добавления приложения из этого диалога комментарий, который не может быть отредактирован, имея удалить запись, если мы хотим, чтобы добавить его снова.

Опция администратора в этом диалоге будет работать не для всех приложений. Работает только для тех, которые позволяют повысить права администратора.

Предупредить тоже 
что в этом диалоге в поле со списком также выйдут те доступы, установленные приложениями, мы можем выбрать их, но некоторые из них не могут быть открыты, давая ошибку.

Комментарий также, что вы должны быть осторожны, потому что в этом списке появятся приложения, которые могут быть для управления или управления приложениями, которые, если мы не знаем, для чего они, лучше не трогать их.

#### Изменить действие < а id= "mark6" > < / а>

Диалог редактирования точно такой же, как добавление действия, но позволит нам 
изменить запись, которую мы выбираем.

Это позволит нам изменить все элементы, кроме тех, которые добавлены с помощью опции добавить установленное приложение, диалоги будут такими же, как в параметрах для добавления.

#### Удалить действие < а id= "mark7" >< / а>

Если мы удалим запись, мы должны иметь в виду, что действие не будет обратимым.

### Кнопка меню < а id= "mark8" >< / а>

Эта кнопка будет доступна из любой точки интерфейса, нажав комбинацию Alt+M.

В этом меню мы найдем четыре подменю 
это категории, действия, создание или восстановление резервных копий и опций, в этом меню мы также находим опцию выход.

Ну категории и действия уже объясните это, так что я объясню подменю сделать и восстановить резервные копии и параметры.

Хорошо, если мы решим сделать резервную копию, откроется окно сохранения Windows, где нам нужно будет выбрать, где сохранить нашу резервную копию базы данных.

Ну имя файла что-то вроде этого по умолчанию:

'Backup-03052021230645. zut-zl`


Ну расширение ставится по умолчанию и имя соответствует модулю и содержит дату, когда он был создан, сказать, что мы можем поставить имя, которое мы хотим.

После сохранения мы можем восстановить его в случае повреждения нашей базы данных или просто удалить ее по ошибке или вернуться к сохраненной версии.

Итак, мы решили восстановить резервные копии, и нам откроется классическое окно Windows для открытия файлов.

Мы должны выбрать копию, которую мы сохранили, которая будет иметь 
расширение*. zut-zl глаз не изменить расширение, потому что, если он не нашел файл.
После выбора резервная копия будет восстановлена, и когда мы нажмем OK, плагин будет закрыт, и в следующий раз, когда мы его откроем, наша копия будет восстановлена.

Прокомментируйте, что файлы *. zut-zl на самом деле являются сжатыми файлами, но будьте осторожны, чтобы изменить их, потому что если они изменены, подпись не будет соответствовать и не позволит восстановить их.

Под этим я подразумеваю, что такие файлы приносят подпись 
это, если он не соответствует при восстановлении даст сбой, и каждая подпись отличается для каждого файла.

В подменю параметров теперь есть только опция вернуться к значениям по умолчанию для запуска приложений.

Если мы выберем эту опцию, вся база данных будет удалена, оставив плагин, как если бы он был недавно установлен.

## Горячие клавиши < а id= "mark9" >< / а>

В двух областях как в категориях, так и в приложениях мы можем сортировать записи с помощью:

* Alt + стрелка вверх или Стрелка вниз


Когда категория или приложение достигнет начала или конца, мы будем объявлены с отличительным звуком, чтобы знать, что мы не можем ни подниматься, ни опускаться дальше.

* Alt + C: быстро приведет нас в область категорий.

* Alt + L: быстро приведет нас к списку приложений.

* Alt + M: откроется меню.

* Клавиша Applications или Shift + F10: в областях категорий и приложений мы развернем контекстное меню с опциями.

* Пробел: в области списка приложений запустите приложение 
пусть у него будет фокус.

* Escape: закрывает все диалоги, которые приложение может открыть даже на главном экране запуска приложений, оставляя нам фокус с того места, где он был вызван.

## Замечания автора < а id= "mark10" > < / а>

Прокомментируйте несколько вещей, первый, когда программа запуска приложений закроется, когда мы запустим одно приложение, придется вызывать его снова, когда мы хотим запустить другое.

А также реализована функция, которая сохранит позицию категории и приложения 
поэтому, когда мы открываем программу запуска приложений, всегда будут выбраны как последняя категория, так и последнее приложение этой категории.

Сохранение фокуса также реализовано, поэтому, когда мы называем программу запуска приложений, она всегда оставляла нас в последнем положении, где фокус был до закрытия.

Например, если фокус находится на кнопке Меню, и мы закрываем пусковую установку приложений, в следующий раз, когда мы открываем его, фокус будет находиться на 
кнопка Меню.

Эти функции действительны только во время сеанса NVDA, это означает, что если мы перезапустим NVDA, мы начнем с фокуса в области категорий.

Этот плагин echo для использования с Windows 10, поэтому, если вы используете более старые версии и у вас есть какие-либо проблемы, прокомментируйте это, но вы, конечно, ничего не сможете сделать, так как некоторые функции можно найти только в Windows 10.

# Модуль быстрые заметки < а id= "mark11" >< / а>

Этот модуль будет служить нам, чтобы иметь под рукой небольшие 
примечания, которые вы можете просматривать, редактировать, удалять.

Этот модуль имеет ту же обработку, что и программа запуска приложений, но различается в некоторых клавишах, описанных ниже.

Я не буду повторять меню, с помощью которого мы можем создавать резервные копии, восстанавливать их, возвращать к значениям по умолчанию плагин, обрабатывать категории и заметки.

Я также не буду повторять обход основного interface, так как это точно то же самое.

Мы можем добавить быструю заметку и в диалоге, что 
он открывается, мы можем поместить название заметки и если мы табулируем содержимое.

Диалог редактирования заметки-это то же самое, поставить заголовок или изменить тот, который уже есть, и иметь возможность редактировать заметку.

Этот модуль отличается от модуля запуска приложений тем, что он использует некоторые новые комбинации клавиш.

* F1: когда мы находимся над заметкой, если мы нажмем F1, он прочитает нам содержимое заметки.
* F2: мы скопируем сфокусированную заметку в буфер обмена, чтобы мы могли всегда копировать ее в любом месте 
и когда приложение, которое поддерживает запись, должно быть сфокусировано, если нет, то ничего не произойдет.
* F3: эта комбинация закроет окно быстрых заметок и вставит содержимое заметки, которое мы сфокусировали на фокусе, то есть вставьте заметку в открытое приложение, если вы позволите вставить текст этого приложения, например, блокнот, поле почты, в Word и т. д.

Это означает, что если мы вызываем модуль быстрые заметки из блокнота или тему 
электронная почта, когда мы нажимаем эту комбинацию текст будет вставлен там, где у нас был фокус.

Например, если мы запустим модуль быстрые заметки с рабочего стола и нажмем F3 поверх заметки, ничего не произойдет, если мы откроем блокнот и нажмем F3, он вставит содержимое заметки в блокнот.

Будьте осторожны, если мы находимся на столе или где-то, где вы не можете вставить прямо, ничего не будет делать.

Он также по-прежнему работает как в области категорий, так и в области списка заметок 
такие области с Alt+стрелки вверх и вниз, чтобы переместить то, что мы выбрали.

Если мы нажмем пробел, откроется окно, в котором мы можем просто отобразить нашу заметку.

Сказать, что этот модуль поставляется без определенной горячей клавиши, поэтому нам придется добавить его в жесты ввода.

Я добавляю в меню Параметры диалог параметров.

В настоящее время у вас есть только один вариант, который выглядит следующим образом:

* Захват заголовка окна в быстрых заметках (из любой точки мира)

Если мы проверим эту опцию 
когда мы нажимаем либо добавить новую быструю заметку, либо новую быструю заметку с выделенным текстом заголовок заметки будет заполнен заголовком окна, которое в данный момент сфокусировано.

# Добавить быструю заметку из любого места < в id= "mark12" > < / в>

Кроме того, модуль быстрых заметок имеет функцию для добавления быстрых заметок с любого сайта без необходимости открывать плагин для добавления.

В диалоговом окне жесты ввода теперь можно настроить новый 
комбинация клавиш, которую вы найдете в:

NVDA / настройки / жесты ввода / zutility / одним нажатием добавляет быструю заметку выделенного текста, двойным нажатием добавляет новую быструю заметку

Когда у нас уже есть назначенная комбинация, вам просто нужно выбрать текст в любом месте и нажать комбинацию клавиш.

Откроется окно, в котором первое, что нам нужно выбрать, это категория, в которой мы хотим сохранить нашу заметку, появятся только категории 
что у нас есть добавленные.

Если мы перейдем в таблицу, мы попадем в поле, чтобы поместить заголовок заметки, и если мы вернемся в таблицу, у нас будет текст, который мы выбрали.

Если мы нажмем OK, он будет сохранен, и у нас уже будет наша записка в нашей выбранной категории.

Если мы дважды нажмем эту комбинацию, откроется тот же экран, но чтобы добавить заметку с нуля. Нам нужно будет выбрать, в какой категории сохранить заметку, название заметки, а также содержимое заметки.

# Виртуальные Меню 
для запуска приложений и для быстрых заметок < а id= "mark13" > < / а>

Ну, эти меню приходят, чтобы расширить возможности, делая его теперь намного более продуктивным и быстрым.

Ну, жесты, которые мы назначили для запуска приложений и быстрых заметок, теперь имеют двойное нажатие.

Если мы нажмем только один раз, эта комбинация выйдет из графического интерфейса, если мы нажмем дважды, мы выйдем из виртуального меню.

В этом меню вы можете перемещаться со стрелками вправо и влево между 
категории и со стрелками вверх и вниз между элементами этой категории, если таковые имеются.

Ну есть некоторые различия между меню запуска приложений и меню быстрых заметок.

В виртуальном меню запуска приложений с помощью стрелок мы перемещаем и с помощью Enter запускаем выбранный элемент, выполняя соответствующее действие.

Если это команда cmd, я бы запустил ее, если это быстрый доступ то же самое, а также если это графический интерфейс.

Хорошо с Escape мы выйдем из меню 
если мы не хотим ничего делать.

Мы также можем перемещаться по категориям, нажимая клавиши запуска имени, за исключением того, что это меню не поддерживается всеми остальными быстро приведет нас к категории.

Хорошо также, если эта буква не имеет категории, она даст нам сообщение о помощи так же, как если бы мы нажали любую другую клавишу, которая отличается от упомянутых.

Сказать, что пока меню активно, все остальные комбинации клавиш NVDA не будут работать, пока мы не выйдем из 
меню.

В меню быстрых заметок клавиша пробела ничего не стоит, и если у вас есть отличия от запуска приложений.

Когда мы находимся над item, если мы нажмем F1, он будет вербализовать содержимое заметки, с F2 мы скопируем заметку в буфер обмена, а с F3 мы вставим содержимое заметки, где у нас есть фокус.

Точно так же, как и в то время как меню этот актив имеет приоритет, пока мы не нажмем клавишу Escape, чтобы покинуть меню, восстановив нормальную функциональность клавиатуры.


## Переводчики и соавторы:<а id= "mark14" > < / а>

* Французский: Реми Руис
* Португальский: Ângelo Мигель Абрантес
* Итальянский: Алессио Ленци
* Хави Домингес: Спасибо, что научили меня программировать меню. Лучше объяснять это для таких дураков, как я.

# Журнал изменений.<а id="mark15"> < /а>
## Версия 0.2.3.<а id="mark0.2. 3"> < /а>

Я добавляю возможность захвата заголовка окон в Добавить новую быструю заметку или добавить быструю заметку выделенного текста.

Эта опция может быть включена 
в меню модуля быстрые заметки в разделе параметры / Параметры.

Если флажок установлен с этого момента, заголовок окна, из которого был вызван создать новую заметку или добавить выделенный текст, будет захвачен.

## Версия 0.2.2.<а id="mark0.2. 2"> < /а>

* Добавлена возможность перемещения между категориями как объектов запуска приложений, так и заметок.
* Добавлено двойное нажатие для клавиши добавить быструю заметку выделенного текста. Теперь с двойным нажатием 
это позволит нам создать новую быструю заметку с нуля.
* Обновленная документация на французском языке.
* Добавлен итальянский язык.

## Версия 0.2.1.<а id="mark0.2. 1"> < /а>

* Исправлена проблема с пустым буфером обмена при желании вставить текст.

## Версия 0.2.<а id="mark0. 2"> < /а>

* Исправлено много внутренних ошибок.
* Я стабилизирую модуль запуска приложений.
* Добавлен новый модуль быстрых заметок.
* Добавлены виртуальные меню для двух модулей.

## Версия 0.1.6.<а id="mark0.1. 6"> < /а>


* Добавлен французский и португальский язык (Португалия / Бразилия).

## Версия 0.1.5.<а id="mark0.1. 5"> < /а>

* Реструктурированные меню.

Добавлена возможность добавления:

* Добавить команду CMD

* Добавить доступ к папкам

* Добавить запуск ярлыков Windows

* Добавить установленное приложение

* Я добавляю на кнопку Меню возможность в настройках вернуться к значениям по умолчанию запуска приложений

* Исправлены различные ошибки с базой данных.

* Исправлены внутренние ошибки.


* Я готовлю плагин для перевода.

## Версия 0.1.<А id="mark0. 1"> < /а>

* Добавлен модуль запуска приложений

* Начальная версия.
