import wx

class JanelaPrincipal(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (900, 550))
		self.criaMenuSuperior()
		self.criaBarraInferior()
		self.criaPanels()

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

	def criaBarraInferior(self):
		self.CreateStatusBar()
		self.SetStatusText('Tudo pronto!')

	def criaPanels(self):
		pEsquerda = PainelEsquerda()
		pDireita = PainelResultados()

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(pEsquerda, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 1)
		sizer.Add(pDireita, 3, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 1)

		self.SetSizer(sizer)


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


class PainelEsquerda(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		mensagem = wx.StaticText(self, -1,
			"Busque uma música, álbum ou artista")
		caixaDeTexto = wx.TextCtrl(self)
		resultadosPesquisa = PainelResultados()

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(mensagem, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(caixaDeTexto, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(resultadosPesquisa, 25, wx.EXPAND | wx.ALL, 1)

		self.SetSizer(sizer)


class PainelResultados(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		mensagem = wx.StaticText(self, -1,
			"Nada para ver aqui", (-1, -1))


class PainelDireita(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		mensagem = StaticText(self, 'Nada para ver aqui')


class Aplicativo(wx.App):
	def OnInit(self):
		frame = JanelaPrincipal(None, 'Caça-Letras')
		frame.Show()
		return True


if __name__ == '__main__':
	app = Aplicativo()
	app.MainLoop()
