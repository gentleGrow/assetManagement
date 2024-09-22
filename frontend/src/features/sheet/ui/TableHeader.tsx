const TableHeader = ({ count, changeCurrency }) => {
  return (
    <div className="flex items-center justify-between pt-[20px]">
      <div className="text-[20px]">
        <span className="font-normal">총</span>{" "}
        <span className="font-bold text-green-60">{count}</span>
        <span className="font-normal">건</span>
      </div>

      <div className="flex items-center space-x-2">
        <span className="color-gray-100 mr-[16px] text-[14px]">
          해외 주식 통화 설정
        </span>
        <button onClick={() => changeCurrency(true)}>₩</button>
        <button onClick={() => changeCurrency(false)}>$</button>
      </div>
    </div>
  );
};

export default TableHeader;
