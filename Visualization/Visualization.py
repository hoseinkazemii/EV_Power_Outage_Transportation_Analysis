from ._plot_travelling_time import plot_travelling_time
from ._plot_distances import plot_distances
from ._plot_queue_length import plot_queue_length


class Visualization():

	def visualize(self, **params):

		plot_travelling_time(**params)
		plot_distances(**params)
		plot_queue_length(**params)
