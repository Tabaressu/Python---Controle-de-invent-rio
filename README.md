Este projeto é um sistema de controle de estoque desenvolvido em Python utilizando Tkinter para a interface gráfica. Ele foi criado com o objetivo de facilitar o gerenciamento de itens em estoque, permitindo que diferentes usuários possam interagir com o sistema de forma controlada, com registro de ações e aprovação de acessos.

O funcionamento é simples: ao abrir a aplicação, o usuário pode se registrar ou realizar login. Novos cadastros ficam pendentes até que um administrador aprove a solicitação. O sistema já vem com um administrador padrão (usuário admin, senha admin) que possui acesso total para visualizar registros e aprovar novos usuários. Os dados de usuários ficam armazenados no arquivo users.json.

Uma vez autenticado, o usuário acessa o menu principal, onde pode consultar o estoque, visualizar o histórico de movimentações, adicionar novos itens ou retirar itens existentes. Todas as movimentações são registradas com data, usuário responsável, quantidade e tipo de ação, e ficam disponíveis para consulta no histórico. Os dados do estoque e histórico são armazenados no arquivo inventory.json, garantindo persistência entre execuções.

A interface foi desenvolvida para ser intuitiva, com janelas simples de navegação e botões para cada funcionalidade. Entre as opções disponíveis no menu principal estão: ver estoque atual, ver histórico de movimentações, retirar item do estoque informando quantidade e data, adicionar novos itens e, para administradores, visualizar registros de usuários e aprovar solicitações de cadastro pendentes.

Para executar o projeto basta ter o Python 3 instalado. Clone o repositório, acesse a pasta do projeto e execute o arquivo principal com o comando python app.py. Não há necessidade de instalar bibliotecas adicionais além das que já vêm com o Python.

Esse sistema pode ser expandido facilmente para incluir novas funcionalidades, como relatórios, exportação de dados ou melhorias visuais. Ele foi desenvolvido para fins de aprendizado, sendo totalmente aberto para modificações e adaptações conforme a necessidade.
