from haystack.signals import RealtimeSignalProcessor


class IndexerSignalProcessor(RealtimeSignalProcessor):
	def handle_save(self,*args,**kwargs):
		RealtimeSignalProcessor.handle_save(self, *args,**kwargs)

	def handle_delete(self,*args,**kwargs):
		RealtimeSignalProcessor.handle_save(self, *args,**kwargs)