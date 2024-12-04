// File: C:\gaon\2024\fast\frontend\src\pages\TimeSeriesPage\timeSeriesPage.tsx
import { useNavigate } from 'react-router-dom';
import { TrendingUp, CloudRain, Activity, Users } from 'lucide-react';
import {
  PageContainer,
  Title,
  CategoryGrid,
  CategoryCard,
  CardIcon,
  CardTitle,
} from './time.style';

const TimeSeriesCategory = () => {
  const navigate = useNavigate();

  const categories = [
    { title: "Stock Market", icon: TrendingUp, path: "/time-series/stock" },
    { title: "Weather Forecast", icon: CloudRain, path: "/time-series/weather" },
    { title: "COVID-19 Trends", icon: Activity, path: "/time-series/covid" },
    { title: "Population Growth", icon: Users, path: "/time-series/population" },
  ];

  const handleCategoryClick = (path: string) => {
    navigate(path);
  };

  return (
    <PageContainer>
      <Title>Time Series Analysis</Title>
      <CategoryGrid>
        {categories.map((category, index) => (
          <CategoryCard 
            key={index} 
            onClick={() => handleCategoryClick(category.path)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <CardIcon>
              <category.icon size={48} />
            </CardIcon>
            <CardTitle>{category.title}</CardTitle>
          </CategoryCard>
        ))}
      </CategoryGrid>
    </PageContainer>
  );
};

export default TimeSeriesCategory;