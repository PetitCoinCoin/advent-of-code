import fs from 'fs';
import { basename } from 'path';
import { argv } from 'process';

import { range } from '../js_utils/utils.js';

class Deck {
	// Of couuuurse it's useless for part 2 XD
	constructor(cards) {
		this.cards = range(0, cards);
		this.count = cards;
	}

	shuffle(shuffleType, param) {
		switch(shuffleType) {
			case 'C':
				this.cut(param);
				break;
			case 'I':
				this.dealWithIncrement(param);
				break;
			case 'N':
				this.cards.reverse();
				break;
			default:
				throw 'wtf'
		}
	}

	cut(n) {
		const sample = n < 0 ? this.count + n : n;
		this.cards = this.cards.splice(sample).concat(this.cards.splice(0, sample));
	}

	dealWithIncrement(n) {
		let shuffled = Array(this.count);
		let i = 0;
		for (const value of this.cards) {
			shuffled[i] = value;
			i = (i + n) % this.count;
		}
		this.cards = [...shuffled];
	}
}

console.time('run');
let data = parseInput();
let cards;
switch (argv[2]) {
	case '1':
		cards = 10007;
		const deck = new Deck(cards);
		for (const instruction of data) {
			deck.shuffle(...instruction);
		};
		console.log(deck.cards.indexOf(2019));
		break
	case '2':
		cards = 119315717514047n;
		const shuffles = 101741582076661n;
		const [inc, off] = composeFunctions();
		// Compose itself
		const increment = mod(exponentiationBySquarring(inc, shuffles), cards);
		const offset = mod(off * (1n - exponentiationBySquarring(inc, shuffles)) * modInv(1n - inc, cards), cards)
		console.log(Number(mod(2020n * increment + offset, cards)));
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
	const regex = /(-?\d+)/g;
	return raw.split('\n').map(line => {
		const digit = line.match(regex);
		if (digit === null) {
			return ['N', 0]
		}
		if (line.includes('cut')) {
			return ['C', digit.map(Number)[0]]
		}
		if (line.includes('with increment')) {
			return ['I', digit.map(Number)[0]]
		}
		throw 'wtf: ' + line
	})
}

function updateLinearParameters(shuffleType, param, inc, off) {
	/***
	 * "cut n": offset shifted by increment * n
	 * "deal with increment n": increment is multiplied by modInv(n)
	 * "deal into new stack": increment is reverserd
	 */
	switch(shuffleType) {
		case 'C':
			return [inc, (off + inc * BigInt(param)) % cards]
		case 'I':
			return [inc * modInv(BigInt(param), cards) % cards, off]
		case 'N':
			return [inc * -1n % cards, off - inc]
		default:
			throw 'wtf: ' + shuffleType
	}
}

function composeFunctions() {
	/***
	 * f(x) = increment * x + offset
	 */
	let [increment, offset] = [1n, 0n];
	for (let i = 0; i < data.length; i++) {
		[increment, offset] = updateLinearParameters(...data[i], increment, offset);
	}
	return [increment, offset]
}

function exponentiationBySquarring(a, n) {
	if (n === 0n) {
		return 1n
	}
	if (n % 2n === 0n) {
		return exponentiationBySquarring(a * a % cards, n / 2n)
	}
	return mod(a * exponentiationBySquarring(a * a % cards, (n - 1n) / 2n), cards)
}

function mod(n, m) {
	return BigInt(((n % m) + m) % m)
}

function modInv(a, n) {
	// returns i such as i * a = 1 % n
	return exponentiationBySquarring(a, n - 2n)
}
