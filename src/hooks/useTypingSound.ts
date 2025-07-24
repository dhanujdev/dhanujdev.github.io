import { useRef, useCallback } from 'react'

export function useTypingSound() {
	const audioContextRef = useRef<AudioContext | null>(null)

	const getAudioContext = useCallback(() => {
		if (!audioContextRef.current) {
			audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
		}
		return audioContextRef.current
	}, [])

	const playTypingSound = useCallback(() => {
		try {
			const audioContext = getAudioContext()
			
			const oscillator = audioContext.createOscillator()
			const gainNode = audioContext.createGain()
			
			oscillator.connect(gainNode)
			gainNode.connect(audioContext.destination)
			
			// Random frequency for typing variation
			oscillator.frequency.setValueAtTime(800 + Math.random() * 400, audioContext.currentTime)
			oscillator.type = 'square'
			
			gainNode.gain.setValueAtTime(0.05, audioContext.currentTime)
			gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.05)
			
			oscillator.start()
			oscillator.stop(audioContext.currentTime + 0.05)
		} catch (error) {
			console.warn('Audio playback failed:', error)
		}
	}, [getAudioContext])

	const playBellSound = useCallback(() => {
		try {
			const audioContext = getAudioContext()
			
			const oscillator = audioContext.createOscillator()
			const gainNode = audioContext.createGain()
			
			oscillator.connect(gainNode)
			gainNode.connect(audioContext.destination)
			
			oscillator.frequency.setValueAtTime(1200, audioContext.currentTime)
			oscillator.type = 'sine'
			
			gainNode.gain.setValueAtTime(0.1, audioContext.currentTime)
			gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.2)
			
			oscillator.start()
			oscillator.stop(audioContext.currentTime + 0.2)
		} catch (error) {
			console.warn('Audio playback failed:', error)
		}
	}, [getAudioContext])

	return { playTypingSound, playBellSound }
}