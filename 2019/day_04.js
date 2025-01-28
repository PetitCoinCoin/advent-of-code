import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let [startRange, endRange] = parseInput();
const range = Array.from({length: endRange + 1 - startRange}, (_, i) => i + startRange);
switch (argv[2]) {
	case '1':
		console.log(range.filter(x => isValid(x, false)).length);
		break
	case '2':
		console.log(range.filter(x => isValid(x, true)).length);
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
	return raw.split('-').map(x => parseInt(x))
}

function isValid(num, isPartTwo) {
	const splitted = String(num).split('').map(Number);
	var double = false;
	var i = 1;
	while (i < splitted.length) {
		if (splitted[i] < splitted[i - 1]){
			return false
		}
		var delta = 1;
		if (!double && splitted[i - 1] == splitted[i]) {
			if (!isPartTwo) {
				double = splitted[i];
			} else {
				while (splitted[i + delta] == splitted[i - 1]) {
					delta++;
				}
				double = delta == 1;
			}
		}
		i += delta;
	}
	return double
}
