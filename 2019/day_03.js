import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

let [wire1, wire2] = parseInput();
const delta = {
	'R': [1, 0],
	'U': [0, 1],
	'L': [-1, 0],
	'D': [0, -1],
}

const {wirePath: path1, fullWirePath: fullPath1} = buildPath(wire1);
const {wirePath: path2, fullWirePath: fullPath2} = buildPath(wire2);
// const crossed = path1.intersection(path2);  >> path1.intersection is not a function ?
const crossed = [...path1].filter(i => path2.has(i));
switch (argv[2]) {
	case '1':
		console.log(getClosest(crossed));
		break
	case '2':
		console.log(getFirst(crossed));
		break
	default:
		throw 'Please set a part to solve (1 or 2)';
}

function readInput() {
	const inputFilename = `inputs/${basename(import.meta.url, '.js')}.txt`;
	return fs
		.readFileSync(inputFilename)
		.toString()
}

function parseInput() {
	let raw = readInput();
	return raw.split('\n').filter(w => w !== '').map(w => w.split(','))
}

function distanceToOrigin(a) {
	return Math.abs(a[0]) + Math.abs(a[1])
}

function buildPath(wire) {
	let wirePath = new Set();
	let fullWirePath = [];
	let x = 0;
	let y = 0;
	wirePath.add(`${x},${y}`);
	fullWirePath.push(`${x},${y}`);
	for (const instruction of wire) {
		let [dx, dy] = delta[instruction[0]];
		let mul = parseInt(instruction.slice(1));
		while (mul > 0) {
			x += dx;
			y += dy;
			wirePath.add(`${x},${y}`);
			fullWirePath.push(`${x},${y}`);
			mul--;
		}
	}
	return {wirePath: wirePath, fullWirePath: fullWirePath}
}

function getClosest(coordinates) {
	return Math.min(...coordinates.map(
		coord => distanceToOrigin(coord.split(',').map(x => parseInt(x)))
	).filter(d => d > 0))
}

function getFirst(coordinates) {
	return Math.min(...coordinates.map(
		coord => fullPath1.indexOf(coord) + fullPath2.indexOf(coord)
	).filter(d => d > 0))
}