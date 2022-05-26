import pyrebase

config = {

}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

n = 0
code = 1
fcode = "{0:04}".format(code)

first_line = "Planta: "

# Create all the .txt files inside firebase database
while n <= 1000:
	path_on_cloud = f"teste/{fcode}.txt"
	local_path = f"txt/{fcode}.txt"
	print(f"path_on_cloud: {path_on_cloud}\nlocal_path: {local_path}\n\n") 
	
	code = code + 1
	fcode = "{0:04}".format(code)
	

	with open(f"txt/{fcode}.txt", "w") as f:
		f.write(str(first_line))

	storage.child(str(path_on_cloud)).put(str(local_path))
	n = n + 1



#path_on_cloud = "teste/0001.txt"
#local_path = "txt/0002.txt"
#storage.child(path_on_cloud).put(local_path)
#storage.child(path_on_cloud).download("test_firebase.txt")
