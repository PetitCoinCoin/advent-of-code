import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
const {data, reversedData} = parseInput();
switch (argv[2]) {
	case '1':
		console.log(countOrbits('COM'));
		break
	case '2':
		const youPath = getOrbitsPath('YOU');
		const sanPath = getOrbitsPath('SAN');
		let pivot;
		for (let p of youPath) {
			if (sanPath.indexOf(p) > -1) {
				pivot = p;
				break
			}
		}
		console.log(youPath.indexOf(pivot) + sanPath.indexOf(pivot) - 2);
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
	let result = {};
	let reversed = {};
	for (const line of raw.split('\n')) {
		const [center, orbit] = line.split(')');
		result[center] ? result[center].push(orbit) : result[center] = [orbit];
		reversed[orbit] = center;
	}
	return {data: result, reversedData: reversed}
}

function countOrbits(planet, parents = 0) {
	return data[planet] ? 
		parents + data[planet].reduce((acc, x) => acc + countOrbits(x, parents + 1), 0)
		:
		parents
}

function getOrbitsPath(planet) {
	let path = [];
	while (planet !== 'COM') {
		path.push(planet);
		planet = reversedData[planet];
	}
	path.push(planet);
	return path
}
