import wx
import model
import wx.lib.scrolledpanel as wxScrll
from pubsub import pub
from threading import Thread


class ThreadSearch(Thread):
	def __init__(self, words):
		Thread.__init__(self)
		self.setDaemon(True)
		self.words = words
		self.start()

	def run(self):
		docs = model.searchDocs(self.words)
		wx.CallAfter( pub.sendMessage, 'docsPanel', docs=docs )
		wx.CallAfter( pub.sendMessage, 'panelState', enable=True )
		wx.CallAfter( pub.sendMessage, 'statusBarMsg', text='Tudo pronto!' )


class ThreadRequest(Thread):
	def __init__(self, doc):
		Thread.__init__(self)
		self.setDaemon(True)
		self.doc = doc
		self.start()

	def run(self):
		model.viewerRoutine(self.doc)
		#wx.CallAfter( pub.sendMessage, 'viewPanel', a definir )


class JanelaPrincipal(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (900, 550))
		self.criaMenuSuperior()
		self.criaBarraInferior()
		self.criaPanels()
		self.SetAutoLayout(1)

		pub.subscribe(self.onStatusBar, 'statusBarMsg')

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
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.pEsquerda = PainelEsquerda(self)
		self.pDireita = PainelDireita(self)
		self.pResultados = PainelResultados(self)

		self.leftSizer.Add(self.pEsquerda, 1, wx.EXPAND | wx.RIGHT, 0)
		self.leftSizer.Add(self.pResultados, 20,  wx.EXPAND | wx.ALL, 0)

		self.mainSizer.Add(self.leftSizer, 1, wx.EXPAND | wx.ALIGN_LEFT
			| wx.RIGHT | wx.TOP | wx.BOTTOM, 1)
		self.mainSizer.Add(self.pDireita, 3, wx.EXPAND | wx.ALIGN_RIGHT
			| wx.LEFT | wx.TOP | wx.BOTTOM, 1)

		self.SetSizer(self.mainSizer)

	# Bindings
	def onStatusBar(self, text):
		self.SetStatusText(text)

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
		wx.Panel.__init__(self, parent = parent)
		
		self.mensagem = wx.StaticText(self, -1,
			"Busque uma música, álbum ou artista")
		self.caixaDeTexto = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
		self.icon = wx.Bitmap('img/kisspng-lupa16.bmp', wx.BITMAP_TYPE_ANY)
		self.searchBtn = wx.BitmapButton(self, bitmap=self.icon, style=wx.BU_TOP)

		self.sizerSearch = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerSearch.Add(self.caixaDeTexto, 6, wx.EXPAND | wx.ALL, 0)
		self.sizerSearch.Add(self.searchBtn, 1, wx.EXPAND | wx.ALL, 0)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.mensagem, 1,
			wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		self.sizer.Add(self.sizerSearch, 1,
			wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

		self.Bind(wx.EVT_BUTTON, self.onSearchBtn, self.searchBtn)
		self.Bind(wx.EVT_TEXT_ENTER, self.onPressEnter, self.caixaDeTexto)
		pub.subscribe(self.onPanelState, 'panelState')

		self.SetSizer(self.sizer)

	# Bindings
	def onPanelState(self, enable):
		if enable:
			self.caixaDeTexto.Enable()
			self.searchBtn.Enable()
		else:
			self.caixaDeTexto.Disable()
			self.searchBtn.Disable()

	def onPressEnter(self, event):
		self.onSearchBtn(event)

	def onSearchBtn(self, event):
		words = self.caixaDeTexto.GetLineText(0)
		pub.sendMessage('panelState', enable=False)
		pub.sendMessage('statusBarMsg', text='Procurando...')
		ThreadSearch(words)


class PainelResultados(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent = parent)
		self.parent = parent
		self.docs = list()

		self.SetAutoLayout(1)
		pub.subscribe(self.onResult, 'docsPanel')

		self.sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Resultados')

		self.list = wx.ListBox(self, size=(100, 700))
		self.Bind(wx.EVT_LISTBOX, self.onSelectListItem, self.list)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onRequestListItem, self.list)

		self.sizer.Add(self.list, 0, wx.ALL | wx.EXPAND, 0)
		self.SetSizerAndFit(self.sizer)

	# Bindings
	def onResult(self, docs):
		if self.docs != []:
			self.list.Clear()
		if docs == None:
			strings = ['Nada encontrado']
		else:
			self.docs = docs
			strings = list()
			for doc in docs:
				string = ' '.join( doc.toString() )
				strings.append(string)

		self.list.InsertItems(strings, 0)
		self.sizer.Layout()

	def onListState(self, event):
		pass

	def onSelectListItem(self, event):
		docsList = event.GetEventObject()
		index = docsList.GetSelection()
		string = docsList.GetString(index)
		pub.sendMessage('statusBarMsg', text='Seleção: ' + string)

	def onRequestListItem(self, event):
		docsList = event.GetEventObject()
		index = docsList.GetSelection()
		ThreadRequest(self.docs[index])


class PainelDireita(wxScrll.ScrolledPanel):
	def __init__(self, parent):
		wxScrll.ScrolledPanel.__init__(self, parent=parent)

		self.SetAutoLayout(1)
		self.SetupScrolling()

		self.mensagem = wx.StaticText(self, label='Nada para ver aqui')
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.mensagem)

		self.SetSizer(self.sizer)

	def onHtmlViewer(self, event):
		pass


class Aplicativo(wx.App):
	def OnInit(self):
		frame = JanelaPrincipal(None, 'Caça-Letras')
		frame.Show()
		return True

def main():
	app = Aplicativo()
	app.MainLoop()

if __name__ == '__main__':
	main()
