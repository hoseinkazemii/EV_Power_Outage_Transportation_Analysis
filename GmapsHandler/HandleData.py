from ._export_distances_and_travelling_time import export_distances_and_travelling_time

class HandleData():

	def preprocess_and_export_results(self, **params):
		
		export_distances_and_travelling_time(**params)
