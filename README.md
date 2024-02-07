# filesDuplicateFinder

[![Codecov](https://codecov.io/gh/DenysonJ/filesDuplicateFinder/graph/badge.svg?token=2771FCYD4R)](https://codecov.io/gh/DenysonJ/filesDuplicateFinder)
![GitHub repo size](https://img.shields.io/github/repo-size/DenysonJ/filesDuplicateFinder)
![GitHub forks](https://img.shields.io/github/forks/DenysonJ/filesDuplicateFinder)
![GitHub open issues](https://img.shields.io/github/issues/DenysonJ/filesDuplicateFinder)


O objetivo desse projeto é desenvolver um programa chamado "filesDuplicateFinder" que permite encontrar e gerenciar arquivos duplicados em diretório, de forma a economizar espaço. O projeto está em desenvolvimento e possui uma lista de tarefas a serem concluídas.

If you don't speak portuguese, open this [translated readme](README-en.md).

:construction: Projeto em construção :construction:

## 📝 Tabela de conteúdos

- [Ajustes e melhorias](#ajustes-e-melhorias)
- [Pré-requisitos](#pré-requisitos)
- [Instalando filesDuplicateFinder](#instalando-filesduplicatefinder)
- [Usando filesDuplicateFinder](#usando-filesduplicatefinder)
- [Contribuindo para filesDuplicateFinder](#contribuindo-para-filesduplicatefinder)
- [Seja um dos contribuidores](#seja-um-dos-contribuidores)
- [Licença](#licença)


### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [X] Criar testes para as principais funções
- [X] Criar flexibilidade para comparação soft em vídeos 
- [ ] Criar sistema de log -> Em desenvolvimento
- [ ] Melhorar performance -> Em desenvolvimento
- [ ] Aumentar cobertura de testes para casos de uso
- [ ] Criar uma Interface Gráfica
- [ ] Criar um instalador
- [ ] Compatibilidade com Windows (não testado ainda)
- [ ] Compatibilidade com macOS (não testado ainda)
- [ ] Compatibilidade com Linux
- [ ] Criar função de similaridade de texto
- [ ] Criar função de similaridade de PDF


## Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou a versão mais recente de `anaconda` ou `miniconda`


## Instalando filesDuplicateFinder

Para instalar o filesDuplicateFinder, instale as dependências necessárias:


``` bash
conda env update --file env.yml
```


## Usando filesDuplicateFinder

Para usar filesDuplicateFinder, siga estas etapas:

Depois de instalar as dependências, ative o ambiente:

``` bash
source activate pythonUtils
```

Ou


``` bash
conda activate pythonUtils
```

Após a ativação do ambiente, execute o programa:

``` bash
python3 duplicateFinder.py -d <caminho_do_diretorio>
```

Com este comando o programa irá procurar por arquivos duplicados no diretório especificado e irá deletar os arquivos duplicados, mantendo apenas um arquivo de cada. A recursividade é desativada por padrão, para ativar a recursividade use a opção `-r` ou `--recursive`. O tipo de comparação é hard por padrão, ou seja, o programa irá comparar os arquivos byte a byte, para usar a comparação soft use a opção `-t` ou `--type` com a opção 'soft'. Para mais informações use a opção `-h` ou `--help`.

Um exemplo de uso do programa, especificando a comparação soft, o limite de similaridade de 0.8, a recursividade, procurando apenas por arquivos com extensão `.mp4` e movendo os arquivos duplicados para a pasta `duplicados`:


``` bash
python3 duplicateFinder.py -d <caminho_do_diretorio> -s 0.8 -t soft -r -i mp4 -a move -o duplicados
```

## Contribuindo para filesDuplicateFinder

Para contribuir com filesDuplicateFinder, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin filesDuplicateFinder / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


## Seja um dos contribuidores

Quer apoiar esse projeto me pagando um café? 


## Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.

[⬆ De volta ao topo](#filesDuplicateFinder)<br>