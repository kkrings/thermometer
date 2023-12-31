from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import grpc.aio  # type: ignore

from sensor.interface.sensor_pb2 import ReadSensorRequest, ReadSensorResponse
from sensor.interface.sensor_pb2_grpc import SensorStub
from sensor.types import SensorReadout


class SensorClient:
    def __init__(self, sensor: SensorStub) -> None:
        self._sensor = sensor

    async def read_sensor(self) -> SensorReadout:
        response: ReadSensorResponse = await self._sensor.ReadSensor(
            ReadSensorRequest()
        )

        return SensorReadout(
            temperature_degree_celsius=response.temperature_degree_celsius,
            relative_humidity_percent=response.relative_humidity_percent,
        )


@asynccontextmanager
async def non_ssl_sensor_connection(host: str) -> AsyncIterator[SensorClient]:
    async with grpc.aio.insecure_channel(target=host) as channel:
        sensor = SensorStub(channel)  # type: ignore
        yield SensorClient(sensor)
