import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
switch (argv[2]) {
	case '1':
		console.log(data);
		break
	case '2':
		throw 'Solve part 1 first ;)';
		break
	default:
		throw 'Please set a part to solve (1 or 2)';
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
	return raw
}
