
from django.shortcuts import render
from django.http import HttpResponse
from sqlalchemy import JSON
from .models import * 
import json
from rest_framework.parsers import JSONParser
from django.http import JsonResponse


################
#Python SDK
###############
import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.crypto import KeyAlgorithm
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import PublicKey
from pycspr import crypto

# Create your views here.
def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.
    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_counter_parties(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the 2 counter-parties participating in the transfer.
    """
    cp1 = pycspr.parse_private_key(
        args.path_to_cp1_secret_key,
        args.type_of_cp1_secret_key,
        )
    cp2 = pycspr.parse_public_key(
        args.path_to_cp2_account_key
        )

    return cp1, cp2

def _get_deploy(args: argparse.Namespace, cp1: PrivateKey, cp2: PublicKey) -> Deploy:
    """Returns transfer deploy to be dispatched to a node.
    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=cp1,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(2.5e9),
        target=cp2.account_key,
        correlation_id=random.randint(1, 1e6)
        )

    return deploy

def send_address(request):
    #Write your script here
    
    data = JSONParser().parse(request)
    
    address = data["publicAddress"]
    pub_address = address["publicAddress"]
    _ARGS = argparse.ArgumentParser("Illustration of how to execute native transfers.")

    _ARGS.add_argument(
        "--cp1-secret-key-path",
        default="E:\Blockchain\Casper\wallet_key\TreasuryAccount_secret_key.pem",
        dest="path_to_cp1_secret_key",
        help="Path to counter-party one's secret_key.pem file.",
        type=str,
        )

    _ARGS.add_argument(
        "--cp1-secret-key-type",
        default="ED25519",
        dest="type_of_cp1_secret_key",
        help="Type of counter party one's secret key.",
        type=str,
        )

    _ARGS.add_argument(
        "--cp2-account-key-path",
        default="E:\Blockchain\Casper\public_keys\omar_pb_key.txt",
        dest="path_to_cp2_account_key",
        help="Path to counter-party two's public_key_hex file.",
        type=str,
        )


    _ARGS.add_argument(
        "--node-host",
        default="136.243.187.84",
        dest="node_host",
        help="Host address of target node.",
        type=str,
        )

    _ARGS.add_argument(
        "--node-port-rpc",
        default="7777",
        dest="node_port_rpc",
        help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
        type=int,
        )

    _ARGS.add_argument(
        "--chain",
        default="casper-test",
        dest="chain_name",
        help="Name of target chain.",
        type=str,
        )

    """
    Put this line to get the args from the cmd
    #args = _ARGS.parse_args()

    Put this line to use argparse without the cmd
    args = _ARGS.parse_args(["--cp1-secret-key-path", "E:\Blockchain\Casper\wallet_key\TreasuryAccount_secret_key.pem", "--cp1-secret-key-type", "ED25519", "--cp2-account-key-path", "E:\Blockchain\Casper\public_keys\omar_pb_key.txt", "--node-host","136.243.187.84", "--node-port-rpc","7777", "--chain", "casper-test"])
    
    """

    args = _ARGS.parse_args(["--cp1-secret-key-path", "E:\Blockchain\Casper\wallet_key\TreasuryAccount_secret_key.pem", "--cp1-secret-key-type", "ED25519", "--cp2-account-key-path", "E:\Blockchain\Casper\public_keys\omar_pb_key.txt", "--node-host","136.243.187.84", "--node-port-rpc","7777", "--chain", "casper-test"])

    client = _get_client(args)

    #cp1 = Treasuery Account
    cp1, cp2 = _get_counter_parties(args)


    # Set deploy.
    deploy: Deploy = _get_deploy(args, cp1, cp2)


    # Approve deploy.
    print("deploy approve started.")
    deploy.approve(cp1)
    print("deploy approve finished.")

    # Dispatch deploy to a node.
    print("send deploy started.")
    client.send_deploy(deploy)
    print("send deploy finished.")

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")

    return HttpResponse("<h1>Done</h1>")


