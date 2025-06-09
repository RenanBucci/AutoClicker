# 🎮 Auto Clicker para Jogos

Um auto clicker profissional desenvolvido em Python com interface gráfica moderna e funcionalidades avançadas, otimizado para jogos como Fortnite.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## ✨ Funcionalidades

- 🎯 **Configuração Flexível**: Intervalo personalizável entre cliques (0.01s até infinito)
- 🖱️ **Múltiplos Tipos de Clique**: Esquerdo, direito ou meio
- ⌨️ **Hotkey Global**: Controle com tecla personalizável (funciona em tela cheia)
- 📍 **Posicionamento Preciso**: Clique em posição fixa ou posição atual do mouse
- 💾 **Configurações Persistentes**: Salva automaticamente suas preferências
- 🎨 **Interface Moderna**: GUI intuitiva e fácil de usar
- 🚀 **Alta Performance**: Otimizado para jogos com baixa latência

## 📸 Screenshots

```
🎮 Auto Clicker para Fortnite
┌─────────────────────────────────────┐
│ Intervalo: [0.1    ] segundos       │
│ Tipo: [Esquerdo ▼]                  │
│ Hotkey: [F6] [Capturar]             │
│ Posição: Atual do mouse             │
│                                     │
│ Status: ▶️ Executando...            │
│                                     │
│ [▶️ Iniciar] [⏹️ Parar] [💾 Salvar] │
└─────────────────────────────────────┘
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/auto-clicker.git
cd auto-clicker
```

### 2. Instale as dependências
```bash
pip install pyautogui pynput
```

**No Windows, se necessário:**
```bash
pip install pywin32
```

### 3. Execute o programa
```bash
python auto_clicker.py
```

## 🎯 Como Usar

### Configuração Básica
1. **Intervalo**: Configure o tempo entre cliques (ex: 0.1 = 10 cliques/segundo)
2. **Tipo de Clique**: Escolha entre esquerdo, direito ou meio
3. **Hotkey**: Defina a tecla para iniciar/parar (padrão: F6)
4. **Posição**: Use posição atual ou defina uma posição fixa

### Controles
- **Iniciar/Parar**: Use os botões da interface ou pressione a hotkey configurada
- **Posição Fixa**: Clique em "Definir Posição" e posicione o mouse onde deseja clicar
- **Salvar Config**: Suas configurações são salvas automaticamente

### Exemplos de Uso

#### Para Jogos FPS (Fortnite, CS:GO)
```
Intervalo: 0.05 (20 cliques/segundo)
Tipo: Esquerdo
Hotkey: F6
Posição: Atual do mouse
```

#### Para Construção Rápida
```
Intervalo: 0.02 (50 cliques/segundo)
Tipo: Esquerdo
Hotkey: F7
Posição: Fixa (ponto específico)
```

#### Para Mineração/Farm
```
Intervalo: 1.0 (1 clique/segundo)
Tipo: Esquerdo
Hotkey: F8
Posição: Fixa
```

## ⚙️ Configurações Avançadas

### Arquivo de Configuração
O programa salva suas configurações em `autoclicker_settings.json`:

```json
{
    "click_interval": "0.1",
    "click_type": "left",
    "hotkey": "f6",
    "click_position": [960, 540]
}
```

### Hotkeys Suportadas
- Teclas alfanuméricas: `a-z`, `0-9`
- Teclas de função: `f1-f12`
- Teclas especiais: `space`, `enter`, `shift`, `ctrl`, `alt`
- Teclas direcionais: `up`, `down`, `left`, `right`

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
auto-clicker/
├── auto_clicker.py          # Arquivo principal
├── autoclicker_settings.json# Configurações (gerado automaticamente)
├── README.md               # Este arquivo
└── requirements.txt        # Dependências
```

### Dependências
- `tkinter` - Interface gráfica (nativo do Python)
- `pyautogui` - Automação de mouse e teclado
- `pynput` - Captura de eventos globais
- `threading` - Execução em paralelo
- `json` - Gerenciamento de configurações

### Contribuindo
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Solução de Problemas

### Erro: ModuleNotFoundError
```bash
# Instale as dependências
pip install pyautogui pynput

# No macOS/Linux, pode ser necessário:
pip3 install pyautogui pynput
```

### Erro de Permissão (Linux/macOS)
```bash
# Execute com sudo se necessário
sudo python3 auto_clicker.py

# Ou instale para o usuário
pip install --user pyautogui pynput
```

### Hotkey não funciona
- Verifique se a tecla não está sendo usada por outro programa
- Execute como administrador no Windows
- No Linux, certifique-se de ter permissões de input

### Cliques muito lentos/rápidos
- Ajuste o intervalo: valores menores = mais rápido
- Mínimo recomendado: 0.01s (100 cliques/segundo)
- Para jogos: teste entre 0.05s a 0.1s

## ⚠️ Aviso Legal

Este software foi desenvolvido para fins educacionais e de automação legítima. O uso em jogos online deve respeitar os termos de serviço de cada plataforma. O desenvolvedor não se responsabiliza pelo uso inadequado da ferramenta.

**Use com responsabilidade:**
- Verifique os termos de uso dos jogos
- Evite vantagens injustas em jogos competitivos
- Respeite outros jogadores

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

Se você gostou do projeto, considere:
- ⭐ Dar uma estrela no repositório
- 🐛 Reportar bugs na aba Issues
- 💡 Sugerir melhorias
- 🤝 Contribuir com código

## 📊 Status do Projeto

- ✅ Interface gráfica completa
- ✅ Hotkeys globais funcionando
- ✅ Múltiplos tipos de clique
- ✅ Posicionamento preciso
- ✅ Configurações persistentes
- 🔄 Em desenvolvimento: Macros personalizados
- 📅 Planejado: Suporte a sequências de cliques

---

**Desenvolvido com ❤️ em Python**

*Última atualização: Junho 2025*
