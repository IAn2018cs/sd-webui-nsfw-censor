from typing import Any, Literal, Dict, TypedDict

import numpy

VisionFrame = numpy.ndarray[Any, Any]

ProcessState = Literal['checking', 'processing', 'stopping', 'pending']
QueuePayload = TypedDict('QueuePayload',
						 {
							 'frame_number': int,
							 'frame_path': str
						 })

LogLevel = Literal['error', 'warn', 'info', 'debug']

ModelValue = Dict[str, Any]

ValueAndUnit = TypedDict('ValueAndUnit',
						 {
							 'value': str,
							 'unit': str
						 })
ExecutionDeviceFramework = TypedDict('ExecutionDeviceFramework',
									 {
										 'name': str,
										 'version': str
									 })
ExecutionDeviceProduct = TypedDict('ExecutionDeviceProduct',
								   {
									   'vendor': str,
									   'name': str,
									   'architecture': str,
								   })
ExecutionDeviceVideoMemory = TypedDict('ExecutionDeviceVideoMemory',
									   {
										   'total': ValueAndUnit,
										   'free': ValueAndUnit
									   })
ExecutionDeviceUtilization = TypedDict('ExecutionDeviceUtilization',
									   {
										   'gpu': ValueAndUnit,
										   'memory': ValueAndUnit
									   })
ExecutionDevice = TypedDict('ExecutionDevice',
							{
								'driver_version': str,
								'framework': ExecutionDeviceFramework,
								'product': ExecutionDeviceProduct,
								'video_memory': ExecutionDeviceVideoMemory,
								'utilization': ExecutionDeviceUtilization
							})
