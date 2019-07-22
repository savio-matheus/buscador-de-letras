import wx

class JanelaPrincipal(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (900, 550))
		self.criaMenuSuperior()
		self.criaConteudo()
		self.criaBarraInferior()
		self.SetBackgroundColour((240, 240, 240))

		self.Show(True)

	def criaMenuSuperior(self):
		opcoesArquivo = wx.Menu()
		opcaoSalvar = opcoesArquivo.Append(wx.ID_SAVE,
			'&Salvar', 'Salva a letra de música selecionada.')
		opcoesArquivo.AppendSeparator()
		opcaoSair = opcoesArquivo.Append(wx.ID_EXIT,
			'S&air', 'Fecha o programa.')

		opcoesSobre = wx.Menu()
		opcaoCreditos = opcoesSobre.Append(1,
			'&Créditos', 'Frameworks e APIs usados no programa.')
		opcaoQuemFez = opcoesSobre.Append(wx.ID_ABOUT,
			'&Quem fez', 'GitHub do (projeto de) desenvolvedor.')

		barraMenus = wx.MenuBar()
		barraMenus.Append(opcoesArquivo, 'Arquivo')
		barraMenus.Append(opcoesSobre, 'Sobre')

		self.Bind(wx.EVT_MENU, self.onSalvar, opcaoSalvar)
		self.Bind(wx.EVT_MENU, self.onSair, opcaoSair)
		self.Bind(wx.EVT_MENU, self.onCreditos, opcaoCreditos)
		self.Bind(wx.EVT_MENU, self.onQuemFez, opcaoQuemFez)

		self.SetMenuBar(barraMenus)

	def criaConteudo(self):
		mensagem = wx.StaticText(self, -1,
			"Busque uma música, álbum ou artista", (-1, -1))
		caixaTexto = wx.TextCtrl(self, )

		# Será alterado quando tiver informações para mostrar
		painelEsquerda = wx.Panel(self)
		painelDireita = wx.Panel(self)

		sizerEsquerda = wx.BoxSizer(wx.VERTICAL)
		sizerEsquerda.Add(mensagem, 1, wx.ALIGN_TOP)
		sizerEsquerda.Add(caixaTexto, 1, wx.ALIGN_TOP | wx.EXPAND, 5)
		sizerEsquerda.Add(painelEsquerda, 25, wx.EXPAND)

		sizerPai = wx.BoxSizer(wx.HORIZONTAL)
		sizerPai.Add(sizerEsquerda, 1, wx.EXPAND | wx.ALIGN_LEFT)
		sizerPai.Add(painelDireita, 3, wx.EXPAND | wx.ALIGN_RIGHT)

		self.SetSizer(sizerPai)

	def criaBarraInferior(self):
		self.CreateStatusBar()
		self.SetStatusText('Tudo pronto!')

	# Bindings -------------------------------------------------------------
	def onSalvar(self, event):
		print('Ainda não faz nada')

	def onSair(self, event):
		self.Destroy()

	def onCreditos(self, event):
		msg = wx.MessageDialog(self,
			'''Um programa para buscar letras de músicas.
			Usa wxPython para a interface gráfica e 
			vagalume.com.br para obter o conteúdo.''',
			'Créditos',
			wx.OK)
		msg.Centre()
		msg.ShowModal()
		msg.Destroy()

	def onQuemFez(self, event):
		msg = wx.MessageDialog(self,
			'Código fonte em https://github.com/savio-matheus',
			'Quem Fez', wx.OK)
		msg.Centre()
		msg.ShowModal()
		msg.Destroy()


if __name__ == '__main__':
	aplicacao = wx.App(False)
	frame = JanelaPrincipal(None, 'Caça-Letras')
	aplicacao.MainLoop()
