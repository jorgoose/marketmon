import type {PageServerLoad} from './$types';

type Data = {
    name: string
    health: number;
    attack: number;
    growth: number;
    defense: number;
}

function generateRandomNumbers(n: number, k: number) {
    if (n > k + 1) {
        throw new Error("n cannot be greater than k + 1");
    }

    const numbers = Array.from({ length: k + 1 }, (_, index) => index);
    const result = [];

    for (let i = 0; i < n; i++) {
        const randomIndex = Math.floor(Math.random() * numbers.length);
        result.push(numbers[randomIndex]);
        numbers.splice(randomIndex, 1);
    }

    return result;
}

export const load: PageServerLoad = async ({fetch}) => {
    const response = await fetch('/data.json');
    const data: Data[] = await response.json();

    const indexes = generateRandomNumbers(8, data.length);

    const cards = indexes.map(i => data[i]);

    return {
        cards
    };
}
