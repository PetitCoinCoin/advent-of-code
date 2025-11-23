import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
switch (argv[2]) {
	case '1':
		console.log(data.map(m => countFuel(m)).reduce((tot, x) => tot + x, 0));
		break
	case '2':
		console.log(data.map(m => recursiveFuel(m)).reduce((tot, x) => tot + x, 0));
		break
	default:
		throw 'Please set a part to solve (1 or 2)'
}
console.timeEnd('run');

function readInput() {
	const inputFilename = `inputs/${basename(import.meta.url, '.js')}.txt`;
	return fs
		.readFileSync(inputFilename)
		.toString()
}

function parseInput() {
	let raw = readInput();
	return raw.split('\n').filter(x => x !== '').map(x => parseInt(x))
}

function countFuel(mass) {
	return Math.floor(mass / 3) - 2
}

function recursiveFuel(mass) {
	const fuel = Math.floor(mass / 3) - 2
	return fuel > 0 ? fuel + recursiveFuel(fuel) : 0
}
