export function isValidAddress(address) {
    return typeof address === 'string' && address.startsWith('Mx') && address.length >= 30;
}

export function isValidAmount(amount) {
    return !isNaN(amount) && Number(amount) > 0;
}

export function isValidTokenId(tokenId) {
    return /^0x[a-fA-F0-9]{64}$/.test(tokenId);
}
