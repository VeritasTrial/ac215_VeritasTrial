import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { ChatCollapsibleHint } from "../../src/components/ChatCollapsibleHint";
import { MdFilterList } from "react-icons/md";

describe("ChatCollapsibleHint", () => {
  it("renders with the correct hint text", () => {
    render(
      <ChatCollapsibleHint
        onToggleHint={vi.fn()}
        hintText="Test Hint"
        HintIcon={MdFilterList}
      >
        Hint Content
      </ChatCollapsibleHint>,
    );

    expect(screen.getByText("Test Hint")).toBeInTheDocument();
  });

  it("renders custom right hint component", () => {
    render(
      <ChatCollapsibleHint
        onToggleHint={vi.fn()}
        hintText="Test Hint"
        HintIcon={MdFilterList}
        rightHintComponent={<button>Custom Button</button>}
      >
        Hint Content
      </ChatCollapsibleHint>,
    );

    expect(screen.getByText("Custom Button")).toBeInTheDocument();
  });

  it("hides collapsible content initially", () => {
    render(
      <ChatCollapsibleHint
        onToggleHint={vi.fn()}
        hintText="Test Hint"
        HintIcon={MdFilterList}
      >
        Hint Content
      </ChatCollapsibleHint>,
    );

    expect(screen.queryByText("Hint Content")).not.toBeInTheDocument();
  });

  it("toggles collapsible content on trigger click", async () => {
    const mockOnToggleHint = vi.fn();

    render(
      <ChatCollapsibleHint
        onToggleHint={mockOnToggleHint}
        hintText="Test Hint"
        HintIcon={MdFilterList}
      >
        Hint Content
      </ChatCollapsibleHint>,
    );

    const trigger = screen.getByText("Test Hint").closest("div");
    expect(trigger).toBeDefined();

    fireEvent.click(trigger!);
    await waitFor(() => {
      expect(screen.queryByText("Hint Content")).toBeInTheDocument();
      expect(mockOnToggleHint).toHaveBeenCalledTimes(1);
    });

    fireEvent.click(trigger!);
    await waitFor(() => {
      expect(screen.queryByText("Hint Content")).not.toBeInTheDocument();
      expect(mockOnToggleHint).toHaveBeenCalledTimes(2);
    });
  });
});
