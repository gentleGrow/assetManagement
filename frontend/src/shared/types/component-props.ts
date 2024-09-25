export interface SegmentedButtonProps {
  numberOfButtons?: number;
  isSelected?: boolean;
  isHover?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
