import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

console.time('run');
let data = {};
parseInput(); 
const oreQuantity = 1000000000000;
const baseQuantity = estimateInput(1);
switch (argv[2]) {
	case '1':
		console.log(baseQuantity);
		break
	case '2':
		console.log(binarySearch(baseQuantity, Math.floor(2 * oreQuantity / baseQuantity)));
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
	const regex = /(\d+) (\w+)/g;
	for (const line of raw.split('\n')) {
		if (line !== '') {
			const items = line.match(regex);
			const [quantity, item] = items.pop().split(' ');
			var material = items.map(x => x.split(' '));
			material.forEach(x => x[0] = parseInt(x[0]));
			data[item] = {
				quantity: parseInt(quantity),
				material: material,
				level: material.length == 1 && material[0][1] === 'ORE' ? 0 : -1,
			}
		}
	}
	while (Object.values(data).some(x => x.level === -1)) {
		for (const value of Object.values(data)) {
			if (value.level === -1) {
				value.level = getLevel(value.material);
			}
		}
	}
}

function getLevel(material) {
	if (material.map(a => data[a[1]].level).some(x => x === -1)) {
		return -1
	}
	return Math.max(...material.map(a => data[a[1]].level)) + 1
}

function estimateInput(fuelQuantity) {
	var currentLevel = Math.max(...Object.values(data).map(x => x.level));
	var needed = {'FUEL': fuelQuantity};
	while (currentLevel >= 0) {
		for (const [key, value] of Object.entries(data)) {
			if (value.level === currentLevel) {
				for (const mat of value.material) {
					needed[mat[1]] = (needed[mat[1]] || 0) + Math.ceil(needed[key] / value.quantity) * mat[0];
				}
			}
		}
		currentLevel -= 1;
	}
	return needed['ORE']
}

function binarySearch(minFuel, maxFuel) {
	if (maxFuel - minFuel == 1) {
		const maxOre = estimateInput(maxFuel);
		return maxOre < oreQuantity ? maxFuel: minFuel
	}
	const midFuel = parseInt((maxFuel + minFuel) / 2);
	const midOre = estimateInput(midFuel);
	if (midOre == oreQuantity) {
		return midFuel
	}
	return midOre > oreQuantity ? binarySearch(minFuel, midFuel) : binarySearch(midFuel, maxFuel)
}
