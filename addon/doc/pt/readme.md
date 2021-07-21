# Manual do ZUtilidades 

O zUtilidades pretende ser um conjunto de pequenos aplicativos para o NVDA.

Tentaremos adicionar aplicativos que possam ser do seu interesse para que possamos consultá-los rapidamente e que por sua vez sejam fáceis de usar e claros na sua interface.

O zUtilidades terá um menu nas Ferramentas do NVDA e nesse menu serão adicionados os diferentes módulos.

Cada módulo vem preparado para podermos adicionar-lhe um atalho, no menu "definir comandos", na categoria zUtilidades.

Por padrão, os módulos virão sem nenhum atalho atribuído.

Portanto, podemos iniciar os módulos indo ao menu Ferramentas / zUtilidades ou atribuindo uma combinação de teclas para cada módulo.

Actualmente é composto pelos seguintes módulos:

* Iniciador de aplicações.

* Notas rápidas.

# Módulo Iniciador de aplicações

Este módulo permite-nos lançar de forma rápida e a partir de qualquer parte do nosso computador uma aplicação, seja portátil ou instalada.

## Ecrã principal

O ecrã principal consiste numa lista de categorias, uma lista de aplicativos e um botão Menu.

Se tabularmos, passaremos pelas diferentes áreas.

### Lista de categorias

Nesta área podemos adicionar, editar ou eliminar uma categoria, podendo ordenar as nossas aplicações ao nosso gosto e por categorias.

Podemos aceder às opções de adicionar, editar ou excluir de duas maneiras.

Enquanto estivermos na área de categorias, pressionando a tecla de aplicativos ou se não tivermos a referida tecla, usando Shift + F10, será mostrado um menu onde podemos escolher uma das 3 opções.

Os diálogos para adicionar e editar são muito simples, tendo um único campo de texto onde podemos colocar o nome da nova categoria ou editar a categoria que escolhermos, dois botões Aceitar e Cancelar.

Se optarmos por apagar, temos que ter em conta que o que aquela categoria contém será apagado completamente sem podermos refazer a acção, portanto tome cuidado para que  não perca os aplicativos que tenha no banco de dados e tenha que refazer a acção.

Também podemos aceder a essas opções clicando no botão Menu ou com a combinação de teclas Alt + M. Se o fizermos, um menu será mostrado com um submenu chamado Categorias onde podemos escolher uma das 3 opções anteriores.

Note que a edição e exclusão estarão sempre na categoria que tem o foco, dando as mensagens correspondentes caso não tenhamos categorias.

Também podemos usar as combinações de teclas Alt + Seta para cima e Seta para baixo para mover a categoria e classificá-la.

### Lista de aplicativos

É nesta área que serão colocadas as aplicações correspondentes à categoria que escolhemos.

Temos 3 opções que são Adicionar acção, Editar acção ou Excluir acção.

Podemos obter essas opções como na lista de categorias com a tecla de aplicativos ou Shift + F10 ou ir ao botão Menu (Alt + M) e procurar o submenu Aplicativos.

Nesta lista de aplicativos, podemos iniciar o aplicativo que está em foco pressionando a tecla de espaço.

Também podemos, com as combinações de teclas Alt + Seta para cima e Seta para baixo, mover a entrada para ordená-los.

Nesta área, podemos navegar rapidamente pelas diferentes entradas, pressionando a primeira letra, de forma que possamos encontrar rapidamente o aplicativo que queremos executar, se tivermos muitos no banco de dados.

#### Adicionar menu de acção

Neste menu podemos escolher entre as seguintes opções:

* Adicionar aplicativo:

Se adicionarmos um aplicativo, existem dois campos que são obrigatórios: o nome do aplicativo e o diretório onde nosso aplicativo está localizado.

Actualmente este extra suporta aplicativos com as extensões exe, bat e com.

Uma vez preenchidos os campos obrigatórios, podemos escolher se o aplicativo requer parâmetros adicionais ou se queremos executar o aplicativo em modo de administrador.

Se quisermos executar um aplicativo no modo de administrador, seremos solicitados a fornecer a permissão correspondente quando iniciarmos o aplicativo.

* Adicionar comando CMD

Nesta caixa de diálogo, podemos adicionar comandos de console.

Os campos de nome para identificar o comando e o campo de comandos são obrigatórios.

Neste caso, além de lançar comandos cmd, se dominarmos o Windows PowerShell, se colocarmos o PowerShell na linha de comando e seguido pelo que queremos, também executaremos comandos do PowerShell.

Da mesma forma, se forem comandos CMD, acrescento que podemos executar várias linhas de comandos que devem ser separadas pelo símbolo (et, &) que se consegue fazer com "shift+6".

Como exemplo, Coloquei uma  linha de comando para reiniciar o Windows explorer, verificará que utilizo o símbolo (et, &) para separar uma linha de comando da outra.

`taskkill /f /im explorer.exe & start explorer`

Nesta caixa de diálogo também podemos colocar uma pausa para que o console não feche e possamos ver os resultados.

Também podemos funcionar como administrador.

* Adicionar acesso à pasta

Nesta caixa de diálogo, teremos que escolher um nome para identificar o acesso à pasta e escolher uma pasta.

Isto  permitirá abrir pastas rapidamente em nosso sistema de qualquer lugar.

* Adicionar atalhos de execução do Windows

Nesta caixa de diálogo, podemos escolher um atalho para iniciá-lo. Também podemos escolher se queremos iniciá-lo como administrador.

Os campos para identificar o nome do atalho e o caminho são obrigatórios.

* Adicionar aplicativo instalado

Nesta caixa de diálogo, todos os aplicativos instalados no nosso computador serão obtidos pelo utilizador ou são aplicativos que já vêm com o Windows.

Também neste ecrã podemos escolher os aplicativos instalados a partir da loja do Windows.

Aviso! isto não é válido para Windows 7.

Uma vez que um aplicativo seja adicionado a partir desta caixa de diálogo, note que ele não pode ser editado, tendo que  se apagar a entrada se quisermos adicioná-lo novamente.

A opção do administrador nesta caixa de diálogo não funcionará para todos os aplicativos. Funcionando apenas para aqueles que permitem usar os privilégios de administrador.

Observe também que nesta caixa de diálogo, os acessos instalados pelos aplicativos também aparecerão na caixa combinada, podemos selecioná-los mas alguns podem não permitir ser abertos, dando um erro.

Note também que tem que ter cuidado porque nesta lista poderá haver aplicativos que podem ser de administração ou gerenciamento que, se não sabemos para que servem, é melhor não mexer neles.

#### Editar acção

A caixa de diálogo de edição é exactamente igual à da ação Adicionar, mas  permitirá modificar a entrada que escolhermos.

Isto  permitir-nos-á modificar todos os elementos, excepto aqueles que foram adicionados pela opção Adicionar aplicativo instalado, as caixas de diálogo serão as mesmas das opções para adicionar.

#### Excluir acção

Se excluirmos uma entrada, devemos ter em mente que a ação não será reversível.

### Botão de menu

Este botão estará acessível de qualquer lugar na interface pressionando a combinação Alt + M.

Neste menu, encontraremos quatro submenus que são Categorias, Ações, Fazer ou restaurar cópias de segurança, Opções e sair.

Categorias e acções  já expliquei, anteriormente, por isso irei explicar apenas o submenu Fazer e restaurar cópias de backup e Opções.

Se escolhermos fazer uma cópia de segurança, abre-se uma janela onde teremos que escolher onde guardar o nosso backup de banco de dados.

Por padrão, o nome do arquivo é mais ou menos assim:

`Backup-03052021230645.zut-zl`

A extensão é configurada por padrão e o nome corresponde ao módulo e contém a data em que foi criado, mas  podemos colocar o nome que quisermos.

Depois de guardado, podemos restaurá-lo caso o nosso banco de dados esteja corrompido ou simplesmente o excluamos por engano ou queiramos  retornar a uma versão que anteriormente tenhamos guardado.

Se optarmos por restaurar as cópias de segurança,  uma janela clássica do Windows será aberta, para nos permitir abrir os respectivos ficheiros.

Temos que escolher a cópia que manteremos, que terá a extensão * .zut-zl, tome cuidado para não alterar a extensão pois caso contrário não encontrará o arquivo.

Uma vez escolhida, a cópia de segurança será restaurada e, quando aceitarmos, o extra será fechado e na próxima vez que o abrirmos, ele terá a nossa cópia restaurada.

Note que os ficheiros * .zut-zl são realmente ficheiros compactados, mas tome cuidado ao modificá-los porque, se forem modificados, a assinatura não corresponderá e não permitirá que sejam restaurados.

No submenu Opções agora há apenas Retornar aos valores padrão no inicializador de aplicativos.

Se escolhermos esta opção, todo o banco de dados será apagado, deixando o add-on como se tivesse acabado de ser instalado.

## Teclas de atalho

Em ambas as áreas, Categorias e Aplicativos, podemos ordenar as entradas com:

* Alt + seta para cima ou seta para baixo

Quando uma categoria ou aplicação atinge o início ou o fim da lista, isso será anunciado com um som distinto para saber que não podemos subir ou descer mais.

* Alt + C:  levará rapidamente para a área de categorias.

* Alt + L:  levará rapidamente para a lista de aplicativos.

* Alt + M: Abre o menu.

* Tecla de aplicativos ou Shift + F10: Nas áreas de categorias e aplicativos mostra o menu com opções.

* Espaço: Na área da lista de aplicativos, será executado o aplicativo que está em foco.

* Escape: fecha todos os diálogos que o aplicativo pode abrir, inclusive o ecrã principal do lançador de aplicações, deixando-nos o foco de onde foi chamado.

## Observações do autor

Tome atenção a várias coisas: a primeira que o Disparador de Aplicativos fechará quando executarmos um aplicativo, tendo que chamá-lo novamente quando quisermos executar outro.

É também implementada uma função que irá guardar a posição da categoria e do último aplicativo visitado, portanto, ao abrirmos o lançador de aplicações, tanto a última categoria quanto o último aplicativo daquela categoria serão sempre os escolhidos.

O  guardar o foco também foi implementado, portanto, quando chamarmos o lançador de aplicações, ele sempre nos deixará na última posição em que o foco estava antes de fechar.

Por exemplo, se o foco estiver no botão de menu e fecharmos o lançador de aplicações, na próxima vez que o abrirmos, o foco estará no botão de menu.

Estas características são válidas apenas durante a sessão do NVDA, isto significa que se reiniciarmos o NVDA  o foco ficará na área de categorias.

Este add-on foi feito para ser usado com o Windows 10, por isso, se  estiver a usar versões anteriores e tiver um problema, comente, mas certamente  não se poderá fazer nada, já que alguns destes recursos só são encontrados no Windows 10.

# Módulo Notas rápidas

Este módulo ajudar-nos-á a ter pequenas notas à mão, as quais  podemos consultar, editar ou excluir.

Este módulo tem o mesmo manuseio que o iniciador de aplicações, mas varia em algumas teclas explicadas abaixo.

Não vou explicar o menu com o qual podemos fazer cópias de segurança, restaurá-las, retornar aos valores padrão do complemento, identificar categorias e notas.

Também não vou explicar a interface principal, porque é exactamente a mesma.

Podemos adicionar uma nota rápida e, no diálogo que é aberto, podemos colocar o título da nota e, se tabularmos, podemos escrever o seu conteúdo.

O diálogo editar nota é exactamente o mesmo, permitindo modificar o título já existente ou modificar a nota.

Este módulo difere do iniciador de aplicações, porque usa algumas novas combinações de teclas.

* F1: Quando estamos no topo de uma nota se pressionarmos F1, leremos o conteúdo da nota.
* F2: copiar a nota focada para  a área de transferência para que possamos colá-la em qualquer lugar.
* F3: Esta combinação fecha a janela de notas rápidas e cola o conteúdo da nota que estava sob o foco.

Isto significa que, se activarmos as notas rápidas no bloco de notas ou num cliente de de -mail quando pressionarmos essa combinação, o texto será colado onde tivermos o foco.

Tenha cuidado: Se estiver numa zona onde não seja permitida a escrita, esta funcionalidade não fará nada.

Também continua a funcionar, tanto na área de categorias quanto na área de listas, para ser capaz de ordenar as referidas áreas com ALT + Setas para cima e para baixo para mover o que selecionarmos.

Se pressionarmos a barra de espaço, será aberta uma janela, na qual só podemos ler a referida nota.

Este módulo vem sem atalho definido, pelo que, se o desejarmos, podemos adicioná-lo em "definições de comandos".

# Adicionar uma nota rápida desde qualquer lugar

Além disso, o módulo de notas rápidas passa a ter um recurso para adicionar notas rápidas de qualquer lugar sem a necessidade de abrir o extra para esse procedimento.

Na caixa de diálogo definir comandos, podemos configurar uma nova combinação de teclas, que encontrará em:

NVDA / Preferências / definir comandos/ Zutilidades / pressionando uma vez, adiciona uma nota rápida do texto selecionado, duas vezes, Adiciona uma nova nota rápida 

Quando já tivermos uma combinação de teclas atribuída, só teremos que seleccionar um texto, em qualquer lugar, e pressionar a combinação de teclas.
Teremos que seleccionar em que categoria queremos adicionar a nota. Só aparecerão as categorias que tenhamos criado.
com "tab", vamos para um campo para escrever e, com outro "tab, ficamos no texto que tínhamos seleccionado".
Se activarmos "aceitar", ficaremos com a nota, dentro da categoria que anteriormente escolhemos.

Se pressionarmos duas vezes a combinação de teclas das notas rápidas, criaremos uma nota em branco, para a qual devemos escolher a categoria, escrever o título e a nota, nos respectivos campos.   

# Menus virtuais para o iniciador de aplicações e para notas rápidas

Estes menus permitirão que o extra seja mais rápido e rpodutivo.

Os atalhos que tivermos adicionado ao iniciador de aplicações e às notas rápidas podem, agora, pressionar-se duas vezes:

Se forem pressionados uma só vez, ficaremos na interface gráfica; Se forem pressionados duas vezes, abrir-se-á o menu virtual.

Neste menu, podemos mover-nos com setas esquerda e direita entre categorias e com as setas para cima e para baixo entre os itens dessa categoria, se os houver.

Há algumas diferenças entre o menu do iniciador de aplicações e o das notas rápidas.

No menu virtual do iniciador de aplicações, com as setas, movemos e introduzimos o item que selecionamos fazendo a ação correspondente.

Se for um comando cmd, eu vou executá-lo, se for um acesso rápido, acontecerá o mesmo como se fosse na interface gráfica.

Pressionar escape, para deixar o menu.

O pressionar das letras permite-nos navegar através do menu.

Diga-se que, enquanto este menu estiver activo, todas as outras combinações de teclas do NVDA não funcionarão, até sairmos do menu.

No menu de notas rápidas, a tecla ""espaço" não é válida.

Quando estamos sobre um item, se pressionarmos F1, ouviremos o conteúdo da nota, com F2 copiaremos a nota para a área de transferência e com F3 colaremos o conteúdo da nota onde tivermos o foco.

## Tradutores e colaboradores:

* Francês: Rémy Ruiz
* Português: Equipa Portuguesa do NVDA
* italiano: Alessio Lenzi
* Javi Domínguez: Mil gracias por enseñarme a programar el menú. Mejor dicho por explicarlo para tontos como yo.

# Modificações.

## Versão 0.2.

* Adicionada a possibilidade de mover ítens entre categorias, tanto no lançador de aplicações como nas notas rápidas.
* Foram corrigidos muitos erros internos;
* Estabilizou-se o iniciador de aplicações
* Adicionou-se o módulo de notas rápidas
* Adicionaram-se menus virtuais para os dois módulos

## Versão 0.1.6.

* Adicionada tradução francês, português.

## Versão 0.1.5.

* Menus reestruturados.

Adicionada a capacidade de adicionar:

* Adicionar comando CMD

* Adicionar acesso à pasta

* Adicionar atalhos de execução do Windows

* Adicionar aplicativo instalado

* Adicionada, no botão de menu, a possibilidade em Opções para retornar o lançador de aplicativos aos valores padrão.

* Corrigidos vários erros com o banco de dados.

* Bugs internos corrigidos.

* O extra foi preparado para ser traduzido.

## Versão 0.1.

* Módulo do iniciador  de aplicações adicionado

* Versão inicial