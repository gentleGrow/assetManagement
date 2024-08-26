import { recipe } from '@vanilla-extract/recipes';
import { heading, text } from '../../../themes/classes/typography';

export const textStyle = recipe({
  variants: {
    fontSize: {
     ...text,
    },
    defaultVariants: {
      fontSize: 'xl',
    },
  }
});


export const headingStyle = recipe({
  variants: {
    fontSize: {
      ...heading,
    },
  },
  defaultVariants: {
    fontSize: "4xl",
  },
});