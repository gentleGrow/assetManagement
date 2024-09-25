export function LeftArrowButton({
  onClick,
  disabled,
}: {
  onClick: () => void;
  disabled: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`group rounded-sm stroke-gray-50 ${disabled ? "" : "hover:bg-[#EFF0F1]"} disabled:stroke-gray-30`}
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M14.5857 4.92893L7.51465 12L14.5857 19.0711"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  );
}

export function RightArrowButton({
  onClick,
  disabled,
}: {
  onClick: () => void;
  disabled: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`group rounded-sm stroke-gray-50 ${disabled ? "" : "hover:bg-[#EFF0F1]"} disabled:stroke-gray-30`}
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M9.89964 4.92893L16.9707 12L9.89964 19.0711"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  );
}

export function ArrowButtons({
  onLeftClick,
  onRightClick,
  leftDisabled,
  rightDisabled,
}: {
  onLeftClick: () => void;
  onRightClick: () => void;
  leftDisabled: boolean;
  rightDisabled: boolean;
}) {
  return (
    <div className="flex h-[24px] w-[48px] rounded-md border border-gray-20">
      <button
        onClick={onLeftClick}
        disabled={leftDisabled}
        className={`flex w-full items-center justify-center stroke-gray-50 ${leftDisabled ? "" : "hover:bg-[#EFF0F1]"} disabled:stroke-gray-30`}
      >
        <svg
          width="7"
          height="12"
          viewBox="0 0 7 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M5.58549 1.05025L0.635742 6L5.58549 10.9497"
            strokeWidth="1.25"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      <div className="w-[1px] bg-gray-20" />

      <button
        onClick={onRightClick}
        disabled={rightDisabled}
        className={`flex w-full items-center justify-center stroke-gray-50 ${leftDisabled ? "" : "hover:bg-[#EFF0F1]"} disabled:stroke-gray-30`}
      >
        <svg
          width="7"
          height="12"
          viewBox="0 0 7 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M1.41451 10.9497L6.36426 6L1.41451 1.05025"
            strokeWidth="1.25"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
    </div>
  );
}
