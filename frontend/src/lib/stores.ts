import { writable } from 'svelte/store';

export const uploadedFile = writable(false);

export const selectedModel = writable('Mushwoom');
