import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ErrorContainer, ErrorMessage, ErrorDescription, GameContainer, Card, CardFront, CardBack } from './loadingFailure.style'

interface LoadingFailureProps {
  message: string;
}

const LoadingFailure = ({ message }: LoadingFailureProps) => {
  const [cards, setCards] = useState<string[]>([]);
  const [flippedIndexes, setFlippedIndexes] = useState<number[]>([]);
  const [matchedPairs, setMatchedPairs] = useState<string[]>([]);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    const symbols = ['🖥️', '📁', '💾', '🔌', '🖱️', '⌨️', '🖨️', '📱'];
    const shuffledCards = [...symbols, ...symbols].sort(() => Math.random() - 0.5);
    setCards(shuffledCards);
  }, []);

  useEffect(() => {
    if (flippedIndexes.length === 2) {
      const [firstIndex, secondIndex] = flippedIndexes;
      if (cards[firstIndex] === cards[secondIndex]) {
        setMatchedPairs((prev) => [...prev, cards[firstIndex]]);
      }
      setTimeout(() => setFlippedIndexes([]), 1000);
    }
  }, [flippedIndexes, cards]);

  useEffect(() => {
    const uniqueMatchedPairs = new Set(matchedPairs);
    if (uniqueMatchedPairs.size === 8) {  // All 8 unique pairs matched
      setIsComplete(true);
    }
  }, [matchedPairs]);

  const flipCard = (index: number) => {
    if (flippedIndexes.length < 2 && !flippedIndexes.includes(index) && !matchedPairs.includes(cards[index])) {
      setFlippedIndexes((prev) => [...prev, index]);
    }
  };

  return (
    <ErrorContainer>
      <ErrorMessage>Oops! Loading Failed</ErrorMessage>
      <ErrorDescription>{message}</ErrorDescription>
      <ErrorDescription>Let's play a game while we fix this!</ErrorDescription>
      <GameContainer>
        {cards.map((card, index) => (
          <Card key={index} onClick={() => flipCard(index)}>
            <motion.div
              initial={false}
              animate={{ rotateY: flippedIndexes.includes(index) || matchedPairs.includes(card) ? 180 : 0 }}
              transition={{ duration: 0.6 }}
              style={{ width: '100%', height: '100%', transformStyle: 'preserve-3d' }}
            >
              <CardFront />
              <CardBack>{card}</CardBack>
            </motion.div>
          </Card>
        ))}
      </GameContainer>
      {isComplete && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <ErrorDescription>Great job! You matched all pairs. Try reloading now!</ErrorDescription>
        </motion.div>
      )}
    </ErrorContainer>
  );
};

export default LoadingFailure;