import type {PageLoad} from './$types';

type Data = {
    [key: string]: {
        health: number;
        attack: number;
        growth: number;
        defense: number;
    }
}

// MMM, AMZN, ALL, BALL, BLK

const filterObject = (data: Data, allowedKeys: string[] = []) => {
  return Object.fromEntries(
    Object.entries(data).filter(([key]) => allowedKeys.includes(key))
  );
};

export const load: PageLoad = async ({fetch}) => {
    const response = await fetch('/data.json');
    const data: Data = await response.json();

    const cards = filterObject(data, ['MMM', 'AMZN', 'BALL', 'ALL', 'BLK'])

    return {
        data: cards
    };
}
