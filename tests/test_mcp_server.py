"""Tests for CryptoGuard MCP Server."""

import json
import pytest
from mcp_server.server import MCPStdioServer, TOOLS, execute_tool


@pytest.fixture
def server():
    return MCPStdioServer()


class TestMCPProtocol:
    def test_initialize(self, server):
        msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = server.handle_message(msg)
        assert resp["result"]["protocolVersion"] == "2024-11-05"
        assert resp["result"]["serverInfo"]["name"] == "cryptoguard"

    def test_tools_list(self, server):
        msg = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = server.handle_message(msg)
        tools = resp["result"]["tools"]
        assert len(tools) == 5
        names = {t["name"] for t in tools}
        assert "cryptoguard_validate_trade" in names
        assert "cryptoguard_scan_token" in names
        assert "cryptoguard_rug_check" in names
        assert "cryptoguard_search" in names
        assert "cryptoguard_health" in names

    def test_ping(self, server):
        msg = {"jsonrpc": "2.0", "id": 3, "method": "ping", "params": {}}
        resp = server.handle_message(msg)
        assert resp["result"] == {}

    def test_unknown_method(self, server):
        msg = {"jsonrpc": "2.0", "id": 4, "method": "unknown/method", "params": {}}
        resp = server.handle_message(msg)
        assert "error" in resp
        assert resp["error"]["code"] == -32601

    def test_notification_returns_none(self, server):
        msg = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        resp = server.handle_message(msg)
        assert resp is None

    def test_resources_list_empty(self, server):
        msg = {"jsonrpc": "2.0", "id": 5, "method": "resources/list", "params": {}}
        resp = server.handle_message(msg)
        assert resp["result"]["resources"] == []


class TestToolDefinitions:
    def test_all_tools_have_required_fields(self):
        for tool in TOOLS:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

    def test_validate_trade_requires_token(self):
        tool = next(t for t in TOOLS if t["name"] == "cryptoguard_validate_trade")
        assert "token" in tool["inputSchema"]["required"]

    def test_rug_check_requires_chain_and_pair(self):
        tool = next(t for t in TOOLS if t["name"] == "cryptoguard_rug_check")
        assert "chain" in tool["inputSchema"]["required"]
        assert "pair_address" in tool["inputSchema"]["required"]


class TestExecuteTool:
    def test_unknown_tool(self):
        result = execute_tool("nonexistent_tool", {})
        assert result["isError"] is True
        assert "Unknown tool" in result["content"][0]["text"]
