import type {PageLoad} from './$types';

type Data = {
    [key: string]: {
        health: number;
        attack: number;
        growth: number;
        defense: number;
    }
}

export const load: PageLoad = async ({fetch}) => {
    const response = await fetch('/data.json');
    const data: Data = await response.json();

    console.log(data);

    return {
        data
    };
}
