import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
let input;
switch (argv[2]) {
	case '1':
		input = 1;
		break
	case '2':
		input = 5;
		break
	default:
		throw 'Please set a part to solve (1 or 2)';
}
intCode();
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
	return raw.split(',').map(Number)
}

function getModes(value) {
	return {
		opcode: value % 100,
		p1: Math.floor((value % 1000) / 100),
		p2: Math.floor((value % 10000) / 1000),
		p3: Math.floor(value / 10000),  // value is not supposed to be on 6 digits
	}
}

function run(i) {
	const {opcode, p1, p2} = getModes(data[i]);
	const param1 = p1 == 1 ? data[i + 1] : data[data[i + 1]];
	const param2 = p2 == 1 ? data[i + 2] : data[data[i + 2]];
	switch (opcode) {
		case 1:
			data[data[i + 3]] = param1 + param2;
			return {isDone: false, step: 4}
		case 2:
			data[data[i + 3]] = param1 * param2;
			return {isDone: false, step: 4}
		case 3:
			data[data[i + 1]] = input;
			return {isDone: false, step: 2}
		case 4:
			console.log(param1);
			return {isDone: false, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 7:
			data[data[i + 3]] = param1 < param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 8:
			data[data[i + 3]] = param1 == param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 99:
			return {isDone: true, step: 0}
		default:
			throw 'wtf'
	}

}

function intCode() {
	let i = 0;
	while (i<data.length) {
		const {isDone, step} = run(i)
		if (isDone) {
			break
		}
		i += step
	}
}
