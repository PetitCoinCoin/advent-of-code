import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
let relativeBase = 0;
let output = '';
let inputs;
switch (argv[2]) {
	case '1':
		// Collected all items, then dropped them methodically to test combinations
		inputs = [...(([
			'south',
			'take astronaut ice cream',
			'north',
			'east',
			'take mouse',
			'north',
			'take spool of cat6',
			'north',
			'take hypercube',
			'east',
			'take sand',
			'south',
			'take antenna',
			'north',
			'west',
			'south',
			'south',
			'south',
			'take mutex',
			'west',
			'take boulder',
			'south',
			'south',
			'south',
			'west',
			'south',
			'inv',
			'drop mutex',
			'drop spool of cat6',
			'drop hypercube',
			// 'drop astronaut ice cream',
			// 'drop boulder',
			'drop antenna',
			// 'drop sand',
			// 'drop mouse',
			'south',
		].join('\n') + '\n'))].map(char => char.codePointAt(0));
		break
	case '2':
		throw 'Solve part 1 first ;)';
		break
	default:
		throw 'Please set a part to solve (1 or 2)';
}
intCode();
console.log(output);
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
	const {opcode, p1, p2, p3} = getModes(data[i]);
	const relativ1 = (p1 == 2 ? data[data[i + 1] + relativeBase] : data[data[i + 1]]) || 0;
	const relativ2 = (p2 == 2 ? data[data[i + 2] + relativeBase] : data[data[i + 2]]) || 0;
	const param1 = p1 == 1 ? data[i + 1] : relativ1;
	const param2 = p2 == 1 ? data[i + 2] : relativ2;
	const param3 = (p3 == 2 ? data[i + 3] + relativeBase : data[i + 3]) || 0;  // should never be in immediate mode
	switch (opcode) {
		case 1:
			data[param3] = param1 + param2;
			return {isDone: false, step: 4}
		case 2:
			data[param3] = param1 * param2;
			return {isDone: false, step: 4}
		case 3:
			if (inputs.length ==  0) {
				console.log(output);
				return {isDone: true, step: 0}
			}
			data[data[i + 1] + (p1 == 2 ? relativeBase : 0)] = inputs.shift();
			return {isDone: false, step: 2}
		case 4:
			output += String.fromCharCode(param1);
			return {isDone: false, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 7:
			data[param3] = param1 < param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 8:
			data[param3] = param1 == param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 9:
			relativeBase += param1;
			return {isDone: false, step: 2}
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
			return
		}
		i += step
	}
}
