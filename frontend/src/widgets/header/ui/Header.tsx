import LogoLink from "./LogoLink";
import Menus from "./Menu";
import Notification from "./Notification";
import Profile from "./Profile";

export default function Header() {
  return (
    <header className="flex h-[64px] w-full items-center justify-around">
      <div className="flex">
        <div className="mr-[120px]">
          <LogoLink />
        </div>
        <Menus />
      </div>
      <div className="flex items-center">
        <div className="ml-[60px] flex space-x-[8px]">
          <Profile />
        </div>
      </div>
    </header>
  );
}
