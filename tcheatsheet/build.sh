#!/bin/bash

cd ./src/src

cargo build --release

cp ./target/release/tcheatsheet ../bin/