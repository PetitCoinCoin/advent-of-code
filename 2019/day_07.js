import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { permute } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
let settingSequences;
let inputs = {};
let programs = {};
let pointers = {};
for (const amp of [0, 1, 2, 3, 4]) {
	programs[amp] = [...data];
	pointers[amp] = 0;
}
var maxThruster = 0;
switch (argv[2]) {
	case '1':
		settingSequences = permute([0, 1, 2, 3, 4]);
		for (const sequence of settingSequences) {
			let signal = 0;
			for (const [amp, value] of sequence.entries()) {
				inputs[amp] = [true, value];
				pointers[amp] = 0;
				signal = intCode(amp, signal);
			}
			maxThruster = Math.max(maxThruster, signal);
		}
		break
	case '2':
		settingSequences = permute([5, 6, 7, 8, 9]);
		for (const sequence of settingSequences) {
			let signal = 0;
			for (const [amp, value] of sequence.entries()) {
				inputs[amp] = [true, value];
				programs[amp] = [...data];
				pointers[amp] = 0;
			}
			while (signal !== null) {
				for (const amp of [0, 1, 2, 3, 4]) {
					signal = intCode(amp, signal);
				}
				maxThruster = Math.max(maxThruster, signal);
			}
		}
		break
		default:
			throw 'Please set a part to solve (1 or 2)';
		}
console.log(maxThruster);
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

function run(i, amp, inputFromPrevious) {
	const {opcode, p1, p2} = getModes(programs[amp][i]);
	const param1 = p1 == 1 ? programs[amp][i + 1] : programs[amp][programs[amp][i + 1]];
	const param2 = p2 == 1 ? programs[amp][i + 2] : programs[amp][programs[amp][i + 2]];
	switch (opcode) {
		case 1:
			programs[amp][programs[amp][i + 3]] = param1 + param2;
			return {output: undefined, step: 4}
		case 2:
			programs[amp][programs[amp][i + 3]] = param1 * param2;
			return {output: undefined, step: 4}
		case 3:
			const [isFirstInput, value] = inputs[amp]
			programs[amp][programs[amp][i + 1]] = isFirstInput ? value : inputFromPrevious;
			inputs[amp] = [false, inputFromPrevious];
			return {output: undefined, step: 2}
		case 4:
			pointers[amp] = i + 2;
			return {output: param1, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {output: undefined, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {output: undefined, step: step}
		case 7:
			programs[amp][programs[amp][i + 3]] = param1 < param2 ? 1 : 0;
			return {output: undefined, step: 4}
		case 8:
			programs[amp][programs[amp][i + 3]] = param1 == param2 ? 1 : 0;
			return {output: undefined, step: 4}
		case 99:
			return {output: null, step: 0}
		default:
			throw 'wtf'
	}

}

function intCode(amp, inputFromPrevious) {
	let i = pointers[amp];
	while (i<programs[amp].length) {
		const {output, step} = run(i, amp, inputFromPrevious)
		if (output !== undefined) {
			return output
		}
		i += step
	}
}
