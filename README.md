if you want to run code within ipython in what I’ll call “small_pyinstall”:
	copy a high-level “import code” to ~/miniconda2/bin (e.g. pdload.py)
		import code_path
		base_code_path = code_path.get(ProjectName)
		sys.path.append(base_code_path)
	add the ProjectName path to ~/.paths.json
