import kivy 
kivy.require('1.11.0')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import pyrebase

#colors
green = (0.55, 0.81, 0.73, 0.5)
dark_green = (0.45, 0.66, 0.6, 0.2)
black = (0.27, 0.29, 0.33, 1)

#green = (150/255, 190/255, 75/255, 0.5)
#dark_green = (150/255, 190/255, 75/255, 1)
#black = (0.27, 0.29, 0.33, 1)

Window.clearcolor = dark_green

config = {

}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

Builder.load_file('code_tree.kv')

class InitialPage(BoxLayout):
	# runs on initialization
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = 'vertical'
		self.spacing = 10

		self.btn1 = Button(text="Escanear Planta",font_size=60, bold=True, background_color=green)
		self.btn1.bind(on_press = self.qrcode_scan)
		self.add_widget(self.btn1)

		self.btn2 = Button(text="Buscar por Código",font_size=60,bold=True,background_color=green)
		self.btn2.bind(on_press = self.code_search)
		self.add_widget(self.btn2)

		#self.btn3 = Button(text="Gerar QRCode")
		#elf.btn1.bind(on_press=self.qrcode_generate)		
		#self.add_widget(self.btn3)         

	def qrcode_scan(self,_):		
		print("Criando tela de scan...")
		PlantaApp.start_scan()
		PlantaApp.screen_manager.current = 'Scan'


	def code_search(self,_):
		print("Criando tela de busca...")
		PlantaApp.start_search()
		PlantaApp.screen_manager.current = 'Search'


class Qr_Scan(BoxLayout):	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.app = App.get_running_app()

		self.orientation = 'vertical'	


		self.render = Builder.load_file('first_cam.kv')			
		self.add_widget(self.render)

		self.search_code = Button(text="Buscar Código",font_size=60, bold=True, background_color=green, size_hint_y=None)
		self.search_code.height = self.search_code.texture_size[1] + 200
		self.search_code.bind(on_press=self.tree_search)
		self.add_widget(self.search_code)	
		
		self.c = Clock.schedule_interval(self._do_setup, 0.1)
				
		
	def _do_setup(self, *l):		
		self.leitura = self.render.ids["label_leitura"].text
		print(len(self.leitura))

		print(f'QR Scan: {self.leitura}')

		if len(self.leitura) is not 0:					
			self.render.ids.tree_code.text = self.leitura[2:6]			

	def tree_search(self,_):
		#Clock.unschedule(self.c)

		self.app = App.get_running_app()	
		print(f"Buscando planta {self.render.ids.tree_code.text} na database...")		
		path_on_cloud = f'teste/{self.render.ids.tree_code.text}.txt'		

		storage.child(path_on_cloud).download(f'{self.render.ids.tree_code.text}.txt')

		self.app.code_storage = self.render.ids.tree_code.text

		try:
			with open(f'{self.render.ids.tree_code.text}.txt') as f:
				d = f.read()			
			PlantaApp.tree_found()			
			PlantaApp.screen_manager.current = 'Tree'
			self.render.ids.tree_code.text = ''		

		except:
			print("Codigo não encontrado")
			PlantaApp.error_found()
			PlantaApp.screen_manager.current = 'Error'
			self.render.ids.tree_code.text = ''
			 

class Code_Search(BoxLayout):	
	def __init__(self, **kwargs):
		super(Code_Search,self).__init__(**kwargs)	
		
		self.orientation = 'vertical'

		self.search_code = Button(
			text="Buscar Código",
			font_size=60,
			bold=True, 
			background_color=green,
			size_hint_y=None,
			height=Window.size[1]*0.6)	

		self.search_code.bind(on_press = self.tree_search)

		self.img = Image(source='icon.png')

		self.add_widget(self.search_code)

		self.add_widget(self.img)

	def tree_search(self,_):
		self.app = App.get_running_app()	
		print(f"Buscando planta {self.ids.codigo_inserido.text} na database...")		
		path_on_cloud = f'teste/{self.ids.codigo_inserido.text}.txt'
		print(path_on_cloud)		

		storage.child(path_on_cloud).download(f'{self.ids.codigo_inserido.text}.txt')

		self.app.code_storage = self.ids.codigo_inserido.text
		print(self.app.code_storage)

		try:
			with open(f'{self.ids.codigo_inserido.text}.txt') as f:
				d = f.read()			
			PlantaApp.tree_found()			
			PlantaApp.screen_manager.current = 'Tree'
			self.ids.codigo_inserido.text = ''			
				

		except:
			print("Codigo não encontrado")
			PlantaApp.error_found()
			PlantaApp.screen_manager.current = 'Error'
			self.ids.codigo_inserido.text = ''	
	


class Error_Page(BoxLayout):
	def __init__(self, **kwargs):
		super(Error_Page, self).__init__(**kwargs)
		self.orientation = 'vertical'			

		self.error_label = Label(
			text= "Código não encontrado\n na database!", 
			font_size=70, 
			bold=True, 
			halign='center',
			color= black
		)
		self.add_widget(self.error_label)

		self.try_again = Button(text= "Tentar outra vez", font_size=60,bold=True, background_color=green)
		self.try_again.bind(on_press=self._again)
		self.add_widget(self.try_again)

	def _again(self,_):
		try:
			PlantaApp.screen_manager.current = 'Scan'
		except: 
			PlantaApp.screen_manager.current = 'Search'



class Tree_Page(BoxLayout):	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.app = App.get_running_app()

		self.orientation = 'vertical'

		self.enviar = Button(
			text="Enviar Modificações",
			font_size=60, bold=True, 
			background_color=green, 
			size_hint_y=None)

		self.enviar.height = self.enviar.texture_size[1] + 200
		self.enviar.bind(on_press=self._submit)
		self.add_widget(self.enviar)		

		Clock.schedule_once(self.after_init, 0.1)	

	def after_init(self, dt):			
		self.app = App.get_running_app()
		with open(f'{self.app.code_storage}.txt') as f:
				d = f.read()

		self.ids.codigo_salvo.text = d


	def _submit(self,_):
		self.app = App.get_running_app()
		self.app.txt = self.ids.codigo_salvo.text		

		PlantaApp.submit_changes()
		PlantaApp.screen_manager.current = 'Submit'

		self.ids.codigo_salvo.text = ''


class Submit_Page(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = 'vertical'

		self.app = App.get_running_app()
		modifications = self.app.txt

		with open(f'{self.app.code_storage}.txt', 'w') as f:
			f.write(str(self.app.txt))		

		path_on_cloud = f'teste/{self.app.code_storage}.txt'
		local_path = f'{self.app.code_storage}.txt'

		storage.child(path_on_cloud).put(local_path)

		self.final_msg = Label(
			text="Arquivo modificado\n com sucesso!", 
			font_size=70, 
			bold=True, 
			halign='center',
			color= black
			)
		self.add_widget(self.final_msg)

		self.back_initial = Button(text="Voltar ao Inicio",font_size=60, bold=True, background_color=green)
		self.back_initial.bind(on_press=self.switch_back)
		self.add_widget(self.back_initial)

	def switch_back(self,_):
		print("De volta ao inicio")
		try:
			for screen in PlantaApp.screen_manager.screens:
				if screen.name == 'Tree':
					PlantaApp.screen_manager.remove_widget(screen)
					PlantaApp.screen_manager.current = 'Scan'	

		
		except:				
			for screen in PlantaApp.screen_manager.screens:
				print(screen.name)
				PlantaApp.screen_manager.clear_widgets(screens=None)					


			PlantaApp.start_search()
			PlantaApp.screen_manager.current = 'Search'


class MinhaPlanta(App):	
	code_storage = ''
	txt = ''
	black = (0.27, 0.29, 0.33, 1)

	def build(self):
		self.icon = 'icon.png'

		self.screen_manager = ScreenManager()		

		self.initial_page = InitialPage()
		screen = Screen(name="Inital")
		screen.add_widget(self.initial_page)
		self.screen_manager.add_widget(screen) 
		
		return self.screen_manager

	def start_scan(self):
		self.scan_page = Qr_Scan()
		screen = Screen(name='Scan')
		screen.add_widget(self.scan_page)
		self.screen_manager.add_widget(screen)  

	def start_search(self):
		self.search_page = Code_Search()
		screen = Screen(name='Search')
		screen.add_widget(self.search_page)
		self.screen_manager.add_widget(screen) 

	def error_found(self):
		self.error_page = Error_Page()
		screen = Screen(name='Error')
		screen.add_widget(self.error_page)
		self.screen_manager.add_widget(screen)

	def tree_found(self):			
		self.tree_page = Tree_Page()
		screen = Screen(name='Tree')
		screen.add_widget(self.tree_page)
		self.screen_manager.add_widget(screen)

	def submit_changes(self):
		self.submit_page = Submit_Page()
		screen = Screen(name='Submit')
		screen.add_widget(self.submit_page)
		self.screen_manager.add_widget(screen)

if __name__ == '__main__':
	PlantaApp = MinhaPlanta()
	PlantaApp.run()
	