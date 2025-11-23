import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = parseInput();
switch (argv[2]) {
	case '1':
		data[1] = 12;
		data[2] = 2;
		console.log(intCode(data)[0]);
		break
	case '2':
		find: {
			for (let noun=0; noun<100; noun++) {
				for (let verb=0; verb<100; verb++){
					let arr = [...data];
					arr[1] = noun;
					arr[2] = verb;
					arr = intCode(arr);
					if (arr[0] == 19690720) {
						console.log(100 * noun + verb);
						break find;
					}
				}
			}
		}
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
	return raw.split(',').map(x => parseInt(x))
}

function run(i, arr) {
	switch (arr[i]) {
		case 1:
			arr[arr[i + 3]] = arr[arr[i + 1]] + arr[arr[i + 2]]
			return false
		case 2:
			arr[arr[i + 3]] = arr[arr[i + 1]] * arr[arr[i + 2]]
			return false
		case 99:
			return true
		default:
			throw 'wtf'
	}

}

function intCode(arr) {
	for (let i=0; i<arr.length; i+=4) {
		if (run(i, arr)) {
			break
		}
	}
	return arr
}
