/**
 * @file RadixMarkdown.tsx
 *
 * Markdown renderer using Radix UI components.
 */

import {
  Blockquote,
  BlockquoteProps,
  Box,
  BoxProps,
  Code,
  CodeProps,
  Em,
  EmProps,
  Heading,
  HeadingProps,
  Link,
  LinkProps,
  ScrollArea,
  Separator,
  SeparatorProps,
  Strong,
  StrongProps,
  Table,
  Text,
  TextProps,
} from "@radix-ui/themes";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";

interface RadixMarkdownProps {
  text: string;
}

const headingCss = {
  paddingTop: "var(--space-4)",
  paddingBottom: "var(--space-3)",
  ":first-child": { paddingTop: 0 },
};

const boxCss = {
  marginBottom: "var(--space-3)",
  ":first-child": { marginTop: 0 },
  ":last-child": { marginBottom: 0 },
};

export const RadixMarkdown = ({ text }: RadixMarkdownProps) => {
  return (
    <Text size="2" as="div">
      <Markdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw, rehypeSanitize]}
        components={{
          // Text-based components
          span: (props) => {
            const { node: _, ...rest } = props;
            return <Text {...(rest as TextProps)}></Text>;
          },
          a: (props) => {
            const { node: _, ...rest } = props;
            return <Link {...(rest as LinkProps)}></Link>;
          },
          em: (props) => {
            const { node: _, ...rest } = props;
            return <Em {...(rest as EmProps)}></Em>;
          },
          strong: (props) => {
            const { node: _, ...rest } = props;
            return <Strong {...(rest as StrongProps)}></Strong>;
          },
          code: (props) => {
            const { node: _, ...rest } = props;
            return <Code variant="ghost" {...(rest as CodeProps)}></Code>;
          },
          label: (props) => {
            const { node: _, ...rest } = props;
            return <Text as="label" {...(rest as TextProps)}></Text>;
          },
          // Block-based components
          div: (props) => {
            const { node: _, ...rest } = props;
            return <Text as="div" {...(rest as TextProps)}></Text>;
          },
          p: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Text as="p" {...(rest as TextProps)}></Text>
              </Box>
            );
          },
          blockquote: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Blockquote {...(rest as BlockquoteProps)}></Blockquote>
              </Box>
            );
          },
          pre: (props) => {
            const { node: _, ...rest } = props;
            return (
              <ScrollArea scrollbars="horizontal" asChild>
                <Box
                  p="2"
                  css={{
                    whiteSpace: "pre",
                    backgroundColor: "var(--gray-a2)",
                    borderRadius: "var(--radius-3)",
                    ...boxCss,
                  }}
                  {...(rest as BoxProps)}
                ></Box>
              </ScrollArea>
            );
          },
          // Heading components
          h1: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h1"
                size="5"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          h2: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h2"
                size="4"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          h3: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h3"
                size="3"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          h4: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h4"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          h5: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h5"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          h6: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Heading
                as="h6"
                css={headingCss}
                {...(rest as HeadingProps)}
              ></Heading>
            );
          },
          // Table components
          table: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Table.Root
                  size="1"
                  variant="ghost"
                  {...(rest as Table.RootProps)}
                ></Table.Root>
              </Box>
            );
          },
          thead: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Table.Header {...(rest as Table.HeaderProps)}></Table.Header>
            );
          },
          tbody: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Body {...(rest as Table.BodyProps)}></Table.Body>;
          },
          tr: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Row {...(rest as Table.RowProps)}></Table.Row>;
          },
          th: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Table.ColumnHeaderCell
                {...(rest as Table.ColumnHeaderCellProps)}
              ></Table.ColumnHeaderCell>
            );
          },
          td: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Cell {...(rest as Table.CellProps)}></Table.Cell>;
          },
          // Misc components
          hr: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Separator size="4" {...(rest as SeparatorProps)}></Separator>
              </Box>
            );
          },
        }}
      >
        {text}
      </Markdown>
    </Text>
  );
};
