/**
 * @file ExternalLink.tsx
 *
 * A link component that opens the link in a new tab.
 */

import { Link, LinkProps } from "@radix-ui/themes";

type ExternalLinkProps = Omit<LinkProps, "rel" | "target"> & {
  href: string;
};

export const ExternalLink = ({
  href,
  children,
  ...props
}: ExternalLinkProps) => {
  return (
    <Link href={href} target="_blank" rel="noreferrer" {...props}>
      {children}
    </Link>
  );
};
