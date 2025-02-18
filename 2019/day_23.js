import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range } from '../js_utils/utils.js';

console.time('run');
let data = parseInput();
const NIC = 50;
const NAT = 255;
let computers = range(0, NIC).reduce((o, key) => ({ ...o, [key]: [...data]}), {});
let relativeBases = range(0, NIC).reduce((o, key) => ({ ...o, [key]: 0}), {});
let starts = range(0, NIC).reduce((o, key) => ({ ...o, [key]: 0}), {});
let inputs = range(0, NIC).reduce((o, key) => ({ ...o, [key]: [key]}), {});
let outputs = range(0, NIC).reduce((o, key) => ({ ...o, [key]: []}), {});
inputs[NAT] = [];
switch (argv[2]) {
	case '1':
		while (inputs[NAT].length < 2) {
			for (const addr of range(0, NIC)) {
				starts[addr] = intCode(starts[addr], addr);
			}
		}
		console.log(inputs[NAT][1]);
		break
	case '2':
		let [prevX, prevY] = [0, 0];
		let [transmittedX, transmittedY] = [null, null];
		let idle = false;
		while (transmittedX !== prevX || transmittedY !== prevY) {
			for (const addr of range(0, NIC)) {
				starts[addr] = intCode(starts[addr], addr);
			}
			idle = range(0, NIC).reduce((tot, key) => tot + inputs[key].length, 0) === 0;
			if (idle) {
				inputs[0] = [...inputs[NAT]];
				[prevX, prevY] = [transmittedX, transmittedY];
				[transmittedX, transmittedY] = inputs[NAT];
				idle = false;
			}
		}
		console.log(transmittedY);
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

function run(i, address) {
	let arr = computers[address];
	const relativeBase = relativeBases[address]
	const {opcode, p1, p2, p3} = getModes(arr[i]);
	const relativ1 = (p1 == 2 ? arr[arr[i + 1] + relativeBase] : arr[arr[i + 1]]) || 0;
	const relativ2 = (p2 == 2 ? arr[arr[i + 2] + relativeBase] : arr[arr[i + 2]]) || 0;
	const param1 = p1 == 1 ? arr[i + 1] : relativ1;
	const param2 = p2 == 1 ? arr[i + 2] : relativ2;
	const param3 = (p3 == 2 ? arr[i + 3] + relativeBase : arr[i + 3]) || 0;  // should never be in immediate mode
	switch (opcode) {
		case 1:
			arr[param3] = param1 + param2;
			return {isDone: false, step: 4}
		case 2:
			arr[param3] = param1 * param2;
			return {isDone: false, step: 4}
		case 3:
			const input = inputs[address].length > 0 ? inputs[address].shift() : -1;
			arr[arr[i + 1] + (p1 == 2 ? relativeBase : 0)] = input;
			return {isDone: input === -1, step: 2}
		case 4:
			outputs[address].push(param1);
			if (outputs[address].length === 3) {
				const inAddress = outputs[address].shift();
				if (inAddress === NAT) {
					inputs[inAddress] = [...outputs[address]];
					outputs[address] = [];
				} else {
					inputs[inAddress] = [...inputs[inAddress], outputs[address].shift(), outputs[address].shift()];
				}
			}
			return {isDone: false, step: 2}
		case 5:
			var step = param1 != 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 6:
			var step = param1 == 0 ? param2 - i : 3;
			return {isDone: false, step: step}
		case 7:
			arr[param3] = param1 < param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 8:
			arr[param3] = param1 == param2 ? 1 : 0;
			return {isDone: false, step: 4}
		case 9:
			relativeBases[address] += param1;
			return {isDone: false, step: 2}
		case 99:
			console.log('stop', address)
			return {isDone: true, step: 0}
		default:
			throw 'wtf: ' + opcode
	}

}

function intCode(start, address) {
	let i = start;
	while (i < computers[address].length) {
		const {isDone, step} = run(i, address)
		if (isDone) {
			return i + step
		}
		i += step
	}
	return 0
}
