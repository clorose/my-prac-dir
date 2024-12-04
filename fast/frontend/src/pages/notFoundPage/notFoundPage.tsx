// File: C:\_YHJ\fast\frontend\src\pages\notFoundPage\notFoundPage.tsx
// Component: notFoundPage
// TypeScript React Component

import React, { useState, useEffect } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import {
  GlobalStyle,
  Container,
  Bubble,
  ErrorCode,
  Message,
  Title,
  Description,
  SubMessage,
  Button,
  TypewriterText
} from './notFound.style';

type AnimatedNumberProps = {
  number: number;
};

const AnimatedNumber = ({ number }: AnimatedNumberProps) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount((prevCount) => {
        if (prevCount < number) {
          return prevCount + 1;
        }
        clearInterval(interval);
        return prevCount;
      });
    }, 30);
    return () => clearInterval(interval);
  }, [number]);

  return <ErrorCode>{count}</ErrorCode>;
};

const NotFoundMessage = () => (
  <Message>
    <Title><AlertTriangle size={20} /> 페이지를 찾을 수 없습니다</Title>
    <Description>
      <TypewriterText>
        요청하신 페이지가 존재하지 않거나 삭제되었을 수 있습니다.
      </TypewriterText>
    </Description>
  </Message>
);

const RefreshButton = () => (
  <Button onClick={() => window.location.href = '/'}>
    <RefreshCw size={20} />
    홈으로 돌아가기
  </Button>
);

const NotFoundPage: React.FC = () => {
  return (
    <>
      <GlobalStyle />
      <Container>
        <Bubble />
        <Bubble />
        <Bubble />
        <AnimatedNumber number={404} />
        <NotFoundMessage />
        <SubMessage>이런! 원하시는 페이지를 찾을 수 없어요.</SubMessage>
        <RefreshButton />
      </Container>
    </>
  );
};

export default NotFoundPage;