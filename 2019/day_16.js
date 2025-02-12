import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
const phases = 100;
switch (argv[2]) {
	case '1':
		var loop = 0;
		while (loop < phases) {
			data = phase();
			loop++;
		}
		console.log(data.slice(0, 8).join(''))
		break
	case '2':
		// Since offset leads us to 2nd half of the data, we have interesting properties.
		// Data prep
		let offset = Number(data.slice(0, 7).join(''));
		const multiply = 10000 - parseInt(offset / data.length);
		offset -= parseInt(offset / data.length) * data.length;
		data = Array(multiply).fill(data).flat().slice(offset)
		// Pattern prep
		var newPattern = Array(data.length).fill(1);
		var loop = 1;
		while (loop < phases) {
			for (let i = 1; i < data.length; i++) {
				newPattern[i] = (newPattern[i] + newPattern[i - 1]) % 10;
			}
			loop++;
		}
		// Calculation
		var res = '';
		for (let k = 0; k < 8; k++) {
			var total = 0;
			for (let i = 0; i < (data.length - k); i++) {
				total += data[i + k] * newPattern[i];
			}
			res += total % 10;
		}
		console.log(res)
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
		.trim()
}

function parseInput() {
	let raw = readInput();
	return raw.split('').map(Number)
}

function getNextElement(idx) {
	var res = 0;
	let sign = 1 ;
	for (let i = idx; i < data.length; i += 2 * (idx + 1)) {
		res += sign * data.slice(i, i + idx + 1).reduce((tot, acc) => tot + acc, 0);
		sign *= -1;
	}
	return Math.abs(res % 10)
}

function phase() {
	var newData = [];
	for (let i=0; i < data.length; i++) {
		newData.push(getNextElement(i));
	}
	return newData
}
