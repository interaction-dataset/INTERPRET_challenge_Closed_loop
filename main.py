#!/usr/bin/python3
import argparse
import logging

import simulator_client
from predictor.echo_predictor import EchoPredictor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("predictor")


def main():
    parser = argparse.ArgumentParser(description='predictor application for prediction-challenge')
    parser.add_argument('-s', '--server',
                        default='127.0.0.1',
                        help='server address to fetch environment state (default: 127.0.0.1).')
    parser.add_argument('-p', '--port',
                        default=50051,
                        help='server port to fetch environment state (default:50051).')
    args = parser.parse_args()

    predictor = EchoPredictor(logger)
    client = simulator_client.SimulatorClient(logger, f'{args.server}:{args.port}', predictor)

    # TODO: If your computer has a fewer number of threads, you can set this fetch_frequency bigger.
    fetch_frequency = 20

    client.start(1 / fetch_frequency)


if __name__ == '__main__':
    main()